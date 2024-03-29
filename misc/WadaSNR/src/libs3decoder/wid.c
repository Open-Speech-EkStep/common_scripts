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
 * wid.c -- Mapping word-IDs between LM and dictionary.
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
 * 26-Feb-2004  A Chan (archan@cs.cmu.edu) at Carnegie Mellon University
 *              Add information to correctly take care class id. 
 *
 * 01-Mar-1999	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Started.
 */


#include "wid.h"

/*ARCHAN 
This loop was first created by Ravi to separate logic which build 
dict->lm and lm->dict mapping to here. I modified it to make it handle 
class-based LM. 
*/

s3lmwid_t *wid_dict_lm_map (dict_t *dict, lm_t *lm,int32 lw)
{
    int32 u, n;
    s3wid_t w,dictid;
    int32 classid = BAD_LMCLASSID;
    s3lmwid_t *map;
    int32 maperr;
    lmclass_word_t lmclass_word;

    maperr=0;

    assert (dict_size(dict) > 0);
    map = (s3lmwid_t *) ckd_calloc (dict_size(dict), sizeof(s3lmwid_t));
    for (n = 0; n < dict_size(dict); n++){
	map[n] = BAD_S3LMWID;
	if(lm->inclass_ugscore)
	  lm->inclass_ugscore[n] = 0; /* Just to be safe, although calloc already did it*/
    }

    n = 0;
    for (u = 0; u < lm_n_ug(lm); u++) {
	w = dict_wordid (dict, lm_wordstr(lm, u));

	if(lm->lmclass)
	  classid=lm_get_classid(lm,lm_wordstr(lm,u));

#if 0
	E_INFO("%d, %s classid %d\n",u,lm_wordstr(lm,u),classid);
#endif
	lm_lmwid2dictwid(lm, u) = w;
	
	if (IS_S3WID(w)) { 
	  if((lm->lmclass)&&(classid!=BAD_LMCLASSID)){    
	    /* It is a valid word and it is also valid class name.
	       Hmm, this causes problem in computing LM probablity.
	       Lets dump more info to allow user know which word(s)
	       have problems.
	    */
	    E_ERROR("%s is both a word and an LM class name\n",lm_wordstr(lm,u));
	    maperr=1;
	  }else{ /* It is a valid word and it is not a class, Ok, it is normal.
		    In Sphinx3, we try to do more checking and try to incorporate alternative 
		    pronounciations. 
		  */
	    if (dict_filler_word (dict, w))
	      E_ERROR("Filler dictionary word '%s' found in LM\n", lm_wordstr(lm, u));
	    
	    if (w != dict_basewid (dict, w)) {
	      E_ERROR("LM word '%s' is an alternative pronunciation in dictionary\n",
		      lm_wordstr(lm, u));
	      
	      w = dict_basewid (dict, w);
	      lm_lmwid2dictwid(lm, u) = w;
	    }
	    
	    for (; IS_S3WID(w); w = dict_nextalt(dict, w))
	      map[w] = (s3lmwid_t) u;
	  }
	} else {
	  if((lm->lmclass)&&(classid!=BAD_LMCLASSID)){ /* it is not a valid word ID but it is a valid class ID */

	    /*	    E_INFO("CLASS INFO: %d, %s\n",classid,lm_wordstr(lm,u));*/
	    lm_lmwid2dictwid(lm, u) = classid;
	    lmclass_word = lmclass_firstword (LM_CLASSID_TO_CLASS(lm,classid));

	    while (lmclass_isword(lmclass_word)) { /*For each word in the class*/
	      dictid = lmclass_getwid(lmclass_word); 

	      /*	      E_INFO("CLASS INFO Inside the word loop: %d, %d, %s\n",dictid,classid,lm_wordstr(lm,u));*/
	      if (dictid >= 0) { 
		if (map[dictid]!=BAD_S3LMWID) {
		  /* 
		   *  This will tell us whether this word is already a normal word,
		   *  Again, we don't do multiple mappings. 
		  */
		  E_INFO("map[dictid] = %d\n",map[dictid]);
		  E_ERROR("Multiple mappings of '%s' in LM\n", lmclass_getword(lmclass_word));
		  maperr = 1;
		} else {

		  if (dict_filler_word (dict, dictid))
		    E_ERROR("Filler dictionary word '%s' found in LM\n", lm_wordstr(lm, dictid));
	    
		  if (dictid != dict_basewid (dict, dictid)) {
		    E_ERROR("LM word '%s' is an alternative pronunciation in dictionary\n",
			    lm_wordstr(lm, dictid));

		    dictid = dict_basewid (dict, dictid);
		  }

		  for (; IS_S3WID(dictid); dictid = dict_nextalt(dict, dictid)){
		    /*		    E_INFO("Inside loop for alternative pronounciations dictid %d %s.\n",dictid,dict_wordstr(dict,dictid));*/
		    map[dictid] = (s3lmwid_t) u; /*Just the normal mapping the unigram space, 
						   The LM file doens't really differentiate between
						   normal word and a class tag */
		    lm->inclass_ugscore[dictid] =
		      lmclass_getprob(lmclass_word)*lw;
		  }
		}

	      } else{
		E_ERROR("%s is a class tag, its word %s but does not appear in dictionary. Dict ID: %d. \n",lm_wordstr(lm,u), lmclass_getword(lmclass_word), dictid);
		n++;
	      }

	      lmclass_word = lmclass_nextword (LM_CLASSID_TO_CLASS(lm,classid),
lmclass_word);
	    }
	  }else{ /*it is not a valid word ID and it is not valid class ID */
	    E_ERROR("%s is not a word in dictionary and it is not a class tag. \n",

lm_wordstr(lm,u)

);
	    n++;
	  }
	}
    }

    if (n > 0)
      E_INFO("%d LM words not in dictionary; ignored\n", n);

    /*    for (n = 0; n < dict_size(dict); n++){
      E_INFO("Index %d, map %d word %s\n",n,map[n],dict_wordstr(dict,n));
      }*/


    
    if(maperr)
      E_FATAL("Error in mapping, please read the log to see why\n");
    
    return map;

    /*    ARCHAN : 20040227, the old routine, it is perfect, so I comment it to make sure everything
	  can roll back.

     n = 0;
    for (u = 0; u < lm_n_ug(lm); u++) {
	w = dict_wordid (dict, lm_wordstr(lm, u));

	classid=lm_get_classid(lm,lm_wordstr(lm,u));

	lm_lmwid2dictwid(lm, u) = w;
	
	if (NOT_S3WID(w)) {
	    n++;
	} else {
	    if (dict_filler_word (dict, w))
		E_ERROR("Filler dictionary word '%s' found in LM\n", lm_wordstr(lm, u));
	    
	    if (w != dict_basewid (dict, w)) {
		E_ERROR("LM word '%s' is an alternative pronunciation in dictionary\n",
			lm_wordstr(lm, u));
		
		w = dict_basewid (dict, w);
		lm_lmwid2dictwid(lm, u) = w;
	    }
	    
	    for (; IS_S3WID(w); w = dict_nextalt(dict, w))
		map[w] = (s3lmwid_t) u;
	}
	}
    if (n > 0)
	E_INFO("%d LM words not in dictionary; ignored\n", n);

    */
    
}


int32 wid_wordprob2alt (dict_t *dict, wordprob_t *wp, int32 n)
{
    int32 i, j;
    s3wid_t w;
    
    for (i = 0, j = n; i < n; i++) {
	w = wp[i].wid;
	for (w = dict_nextalt (dict, w); IS_S3WID(w); w = dict_nextalt (dict, w)) {
	    wp[j].wid = w;
	    wp[j].prob = wp[i].prob;
	    j++;
	}
    }
    
    return j;
}
