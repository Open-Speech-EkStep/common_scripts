/* ====================================================================
 * Copyright (c) 1999-2004 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer. 
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced 
 * Research Projects Agency and the National Science Foundation of the 
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND 
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 *
 */
/*
 * bio.c -- Sphinx-3 binary file I/O functions.
 * 
 * **********************************************
 * CMU ARPA Speech Project
 *
 * Copyright (c) 1996 Carnegie Mellon University.
 * ALL RIGHTS RESERVED.
 * **********************************************
 * 
 * HISTORY
 * 
 * 02-Jul-1997	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Bugfix: Added byteswapping in bio_verify_chksum().
 * 
 * 18-Dec-1996	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Created.
 */


#include "bio.h"


#define BIO_HDRARG_MAX	32
#define END_COMMENT	"*end_comment*\n"


static void bcomment_read (FILE *fp)
{
    char iline[16384];

    while (fgets(iline, sizeof(iline), fp) != NULL) {
	if (strcmp(iline, END_COMMENT) == 0)
	    return;
    }
    E_FATAL("Missing %s marker\n", END_COMMENT);
}


static int32 swap_check(FILE *fp)
{
    uint32 magic;

    if (fread(&magic, sizeof(uint32), 1, fp) != 1) {
	E_ERROR ("Cannot read BYTEORDER MAGIC NO.\n");
	return -1;
    }

    if (magic != BYTE_ORDER_MAGIC) {
	/* either need to swap or got bogus magic number */
	SWAP_INT32(&magic);
	
	if (magic == BYTE_ORDER_MAGIC)
	    return 1;

	SWAP_INT32(&magic);
	E_ERROR("Bad BYTEORDER MAGIC NO: %08x, expecting %08x\n",
		magic, BYTE_ORDER_MAGIC);
	return -1;
    }

    return 0;
}


void bio_hdrarg_free (char **argname, char **argval)
{
    int32 i;
    
    for (i = 0; argname[i]; i++) {
	ckd_free (argname[i]);
	ckd_free (argval[i]);
    }
    ckd_free (argname);
    ckd_free (argval);
}


int32 bio_writehdr_version (FILE *fp, char *version)
{
    uint32 b;
    
    fprintf (fp, "s3\n");
    fprintf (fp, "version %s\n", version);
    fprintf (fp, "endhdr\n");
    fflush (fp);
    
    b = (uint32) BYTE_ORDER_MAGIC;
    fwrite (&b, sizeof(uint32), 1, fp);
    fflush (fp);
    
    return 0;
}


int32 bio_readhdr (FILE *fp, char ***argname, char ***argval, int32 *swap)
{
    char line[16384], word[4096];
    int32 i, l;
    int32 lineno;
    
    *argname = (char **) ckd_calloc (BIO_HDRARG_MAX+1, sizeof(char *));
    *argval = (char **) ckd_calloc (BIO_HDRARG_MAX, sizeof(char *));

    lineno = 0;
    if (fgets (line, sizeof(line), fp) == NULL)
	E_FATAL("Premature EOF, line %d\n", lineno);
    lineno++;
    
    if ((line[0] == 's') && (line[1] == '3') && (line[2] == '\n')) {
	/* New format (post Dec-1996, including checksums); read argument-value pairs */
	for (i = 0;;) {
	    if (fgets (line, sizeof(line), fp) == NULL)
		E_FATAL("Premature EOF, line %d\n", lineno);
	    lineno++;
	    
	    if (sscanf (line, "%s%n", word, &l) != 1)
		E_FATAL("Header format error, line %d\n", lineno);
	    if (strcmp (word, "endhdr") == 0)
		break;
	    if (word[0] == '#')		/* Skip comments */
		continue;

	    if (i >= BIO_HDRARG_MAX)
		E_FATAL("Max arg-value limit(%d) exceeded; increase BIO_HDRARG_MAX\n",
			BIO_HDRARG_MAX);
	    
	    (*argname)[i] = ckd_salloc (word);
	    if (sscanf (line+l, "%s", word) != 1)	/* Multi-word values not allowed */
		E_FATAL("Header format error, line %d\n", lineno);
	    (*argval)[i] = ckd_salloc (word);
	    i++;
	}
    } else {
	/* Old format (without checksums); the first entry must be the version# */
	if (sscanf(line, "%s", word) != 1)
	    E_FATAL("Header format error, line %d\n", lineno);

	(*argname)[0] = ckd_salloc ("version");
	(*argval)[0] = ckd_salloc (word);
	i = 1;
	
	bcomment_read(fp);
    }
    (*argname)[i] = NULL;
    
    if ((*swap = swap_check(fp)) < 0)
	E_FATAL("swap_check failed\n");

    return 0;
}


static uint32 chksum_accum (void *buf, int32 el_sz, int32 n_el, uint32 sum)
{
    int32 i;
    uint8 *i8;
    uint16 *i16;
    uint32 *i32;
    
    switch (el_sz) {
    case 1:
	i8 = (uint8 *)buf;
	for (i = 0; i < n_el; i++)
	    sum = (sum << 5 | sum >> 27) + i8[i];
	break;
    case 2:
	i16 = (uint16 *)buf;
	for (i = 0; i < n_el; i++)
	    sum = (sum << 10 | sum >> 22) + i16[i];
	break;
    case 4:
	i32 = (uint32 *)buf;
	for (i = 0; i < n_el; i++)
	    sum = (sum << 20 | sum >> 12) + i32[i];
	break;
    default:
	E_FATAL("Unsupported elemsize for checksum: %d\n", el_sz);
	break;
    }

    return sum;
}


static void swap_buf (void *buf, int32 el_sz, int32 n_el)
{
    int32 i;
    uint16 *buf16;
    uint32 *buf32;

    switch (el_sz) {
    case 1:
	break;
    case 2:
	buf16 = (uint16 *) buf;
	for (i = 0; i < n_el; i++)
	    SWAP_INT16(buf16+i);
	break;
    case 4:
	buf32 = (uint32 *) buf;
	for (i = 0; i < n_el; i++)
	    SWAP_INT32(buf32+i);
	break;
    default:
	E_FATAL("Unsupported elemsize for byteswapping: %d\n", el_sz);
	break;
    }
}


int32 bio_fread (void *buf, int32 el_sz, int32 n_el, FILE *fp, int32 swap, uint32 *chksum)
{
    if (fread (buf, el_sz, n_el, fp) != (size_t)n_el)
	return -1;
    
    if (swap)
	swap_buf (buf, el_sz, n_el);
    
    if (chksum)
	*chksum = chksum_accum (buf, el_sz, n_el, *chksum);

    return n_el;
}


int32 bio_fread_1d (void **buf, int32 el_sz, int32 *n_el, FILE *fp, int32 sw, uint32 *ck)
{
    if ((el_sz != 1) && (el_sz != 2) && (el_sz != 4))
	E_FATAL("Unsupported elemsize: %d\n", el_sz);
    
    /* Read 1-d array size */
    if (bio_fread (n_el, sizeof(int32), 1, fp, sw, ck) != 1)
	E_FATAL("fread(arraysize) failed\n");
    if (*n_el <= 0)
	E_FATAL("Bad arraysize: %d\n", *n_el);
    
    /* Allocate memory for array data */
    *buf = (void *) ckd_calloc (*n_el, el_sz);

    /* Read array data */
    if (bio_fread (*buf, el_sz, *n_el, fp, sw, ck) != *n_el)
	E_FATAL("fread(arraydata) failed\n");

    return *n_el;
}


void bio_verify_chksum (FILE *fp, int32 byteswap, uint32 chksum)
{
    uint32 file_chksum;
    
    if (fread (&file_chksum, sizeof(uint32), 1, fp) != 1)
	E_FATAL("fread(chksum) failed\n");
    if (byteswap)
	SWAP_INT32(&file_chksum);
    if (file_chksum != chksum)
	E_FATAL("Checksum error; file-checksum %08x, computed %08x\n",
		file_chksum, chksum);
}
