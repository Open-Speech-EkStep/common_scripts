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
 * heap.c -- Generic heap structure for inserting in any and popping in sorted
 * 		order.
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
 * 23-Dec-96	M K Ravishankar (rkm@cs.cmu.edu) at Carnegie Mellon University
 * 		Started.
 */


#ifndef _LIBUTIL_HEAP_H_
#define _LIBUTIL_HEAP_H_

#include "prim_type.h"

  /** \file heap.h
   * \brief Heap Implementation. 
   *
   * General Comment: Sorted heap structure with three main operations:
   * 
   *   1. Insert a data item (with two attributes: an application supplied pointer and an
   *      integer value; the heap is maintained in ascending order of the integer value).
   *   2. Return the currently topmost item (i.e., item with smallest associated value).
   *   3. Return the currently topmost item and pop it off the heap.
   */

#ifdef __cplusplus
extern "C" {
#endif

typedef void *heap_t;




  /**
   * Allocate a new heap and return handle to it.
   */
heap_t heap_new ( void );


  /**
   * Insert a new item into the given heap.
   * Return value: 0 if successful, -1 otherwise.
   */
int32 heap_insert (heap_t heap,	/* In: Heap into which item is to be inserted */
		   void *data,	/* In: Application-determined data pointer */
		   int32 val);	/* In: According to item entered in sorted heap */

  /**
   * Return the topmost item in the heap.
   * Return value: 1 if heap is not empty and the topmost value is returned;
   * 0 if heap is empty; -1 if some error occurred.
   */
int32 heap_top (heap_t heap,	/* In: Heap whose topmost item is to be returned */
		void **data,	/* Out: Data pointer associated with the topmost item */
		int32 *val);	/* Out: Value associated with the topmost item */

  /**
   * Like heap_top but also pop the top item off the heap.
   */
int32 heap_pop (heap_t heap, void **data, int32 *val);


  /**
   * Destroy the given heap; free the heap nodes.  NOTE: Data pointers in the nodes are NOT freed.
   * Return value: 0 if successful, -1 otherwise.
   */

int32 heap_destroy (heap_t heap);

#ifdef __cplusplus
}
#endif

#endif
