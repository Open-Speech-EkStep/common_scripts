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
 * s3types.h -- Types specific to s3 decoder.
 *
 * **********************************************
 * CMU ARPA Speech Project
 *
 * Copyright (c) 1999 Carnegie Mellon University.
 * ALL RIGHTS RESERVED.
 * **********************************************
 * 
 * HISTORY
 * 
 * 13-May-1999	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University.
 * 		Changed typedef source for s3ssid_t from int32 to s3pid_t.
 * 		Changed s3senid_t from int16 to int32 (to conform with composite senid
 * 		which is int32).
 * 
 * 04-May-1999	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University.
 * 		Added senone sequence ID (s3ssid_t).
 * 
 * 12-Jul-95	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University.
 * 		Started.
 */


#ifndef _S3_S3TYPES_H_
#define _S3_S3TYPES_H_

#include <libutil/libutil.h>
#include <float.h>

/** \file s3types.h
 * \brief Size definition of semantically units. Common for both s3 and s3.X decoder. 
 */

#ifdef __cplusplus
extern "C" {
#endif

  /**
 * Size definitions for more semantially meaningful units.
 * Illegal value definitions, limits, and tests for specific types.
 * NOTE: Types will be either int32 or smaller; only smaller ones may be unsigned (i.e.,
 * no type will be uint32).
 */

typedef int16		s3cipid_t;	/** Ci phone id */
#define BAD_S3CIPID	((s3cipid_t) -1)
#define NOT_S3CIPID(p)	((p)<0)
#define IS_S3CIPID(p)	((p)>=0)
#define MAX_S3CIPID	127

typedef int32		s3pid_t;	/** Phone id (triphone or ciphone) */
#define BAD_S3PID	((s3pid_t) -1)
#define NOT_S3PID(p)	((p)<0)
#define IS_S3PID(p)	((p)>=0)
#define MAX_S3PID	((int32)0x7ffffffe)

typedef s3pid_t		s3ssid_t;	/** Senone sequence id (triphone or ciphone) */
#define BAD_S3SSID	((s3ssid_t) -1)
#define NOT_S3SSID(p)	((p)<0)
#define IS_S3SSID(p)	((p)>=0)
#define MAX_S3SSID	((int32)0x7ffffffe)

typedef int32		s3tmatid_t;	/** Transition matrix id; there can be as many as pids */
#define BAD_S3TMATID	((s3tmatid_t) -1)
#define NOT_S3TMATID(t)	((t)<0)
#define IS_S3TMATID(t)	((t)>=0)
#define MAX_S3TMATID	((int32)0x7ffffffe)

typedef int32		s3wid_t;	/** Dictionary word id */
#define BAD_S3WID	((s3wid_t) -1)
#define NOT_S3WID(w)	((w)<0)
#define IS_S3WID(w)	((w)>=0)
#define MAX_S3WID	((int32)0x7ffffffe)

typedef uint16		s3lmwid_t;	/** LM word id (uint16 for conserving space) */
#define BAD_S3LMWID	((s3lmwid_t) 0xffff)
#define NOT_S3LMWID(w)	((w)==BAD_S3LMWID)
#define IS_S3LMWID(w)	((w)!=BAD_S3LMWID)
#define MAX_S3LMWID	((uint32)0xfffe)
#define BAD_LMCLASSID   (-1)

typedef int32		s3latid_t;	/** Lattice entry id */
#define BAD_S3LATID	((s3latid_t) -1)
#define NOT_S3LATID(l)	((l)<0)
#define IS_S3LATID(l)	((l)>=0)
#define MAX_S3LATID	((int32)0x7ffffffe)

typedef int16   	s3frmid_t;	/** Frame id (must be SIGNED integer) */
#define BAD_S3FRMID	((s3frmid_t) -1)
#define NOT_S3FRMID(f)	((f)<0)
#define IS_S3FRMID(f)	((f)>=0)
#define MAX_S3FRMID	((int32)0x7ffe)

typedef int16   	s3senid_t;	/** Senone id */
#define BAD_S3SENID	((s3senid_t) -1)
#define NOT_S3SENID(s)	((s)<0)
#define IS_S3SENID(s)	((s)>=0)
#define MAX_S3SENID	((int16)0x7ffe)

typedef int16   	s3mgauid_t;	/** Mixture-gaussian codebook id */
#define BAD_S3MGAUID	((s3mgauid_t) -1)
#define NOT_S3MGAUID(m)	((m)<0)
#define IS_S3MGAUID(m)	((m)>=0)
#define MAX_S3MGAUID	((int32)0x00007ffe)


#define S3_START_WORD		"<s>"
#define S3_FINISH_WORD		"</s>"
#define S3_SILENCE_WORD		"<sil>"
#define S3_UNKNOWN_WORD		"<UNK>"
#define S3_SILENCE_CIPHONE	"SIL"

#define S3_LOGPROB_ZERO		((int32) 0xc8000000)	/** Integer version of log of zero Approx -infinity!! */
#define S3_LOGPROB_ZERO_F	((float32) -1e30)	/** Float version of log of zero Approx -infinity!! */

/* RAH, I believe this is unreasonably large and not feasible */ /* Frame = 10msec */
/* #define S3_MAX_FRAMES		30000   */ /* Frame = 10msec */  
#define S3_MAX_FRAMES		15000    /* RAH, I believe this is still too large, but better than before */

#define RENORM_THRESH     ((int32) ((S3_LOGPROB_ZERO)>>1))       /** Bestscore getting close to 0 */

#define S3_SUCCESS      0
#define S3_ERROR        -1
#define S3_WARNING      -2

  /** The maximum # of states for any given acoustic model */
#define MAX_N_STATE     20

  /** The maximum # of attributes associated with any
 * given acoustic model */
#define MAX_N_ATTRIB    5

#ifndef TRUE
#define TRUE  1
#define FALSE 0 /* assume that true is never defined w/o false */
#endif

/* Timer for elapsed I/O time */
#define IO_ELAPSED      0

/* Timer for utt processing elapsed time */
#define UTT_ELAPSED     1
#define UTT_IO_ELAPSED  2
#define UTT_BW_ELAPSED  3

#define TYING_NON_EMITTING      (0xffffffff)
#define TYING_NO_ID             (0xffffffff)

#define MAX_VERSION_LEN 128

#define MEG *1024*1024

#ifdef __cplusplus
}
#endif

#endif
