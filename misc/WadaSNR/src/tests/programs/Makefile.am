LIVEDECSRCS = parse_args_file.c \
		fe_dump.c \
		feat_dump.c \
		fe_sigproc_dump.c \
		live_dump.c \
		metrics.c

LIVEDECOBJS = $(LIVEDECSRCS:.c=.o) 


noinst_PROGRAMS = lm_test \
		  lm_utt_test \
		  dumpfrontend  

noinst_HEADERS = cmd_ln_args.h \
	fe_dump.h \
	fe_internal_dump.h \
	feat_dump.h \
	live_dump.h \
	metrics.h

dumpfrontend_SOURCES = dump_frontend.c \
			${LIVEDECSRCS}

#batchmetrics_SOURCES = batch_metrics.c \
#			${LIVEDECSRCS}

lm_test_SOURCES = lm_test.c \
			${LIVEDECSRCS}

lm_utt_test_SOURCES = lm_utt_test.c \
			${LIVEDECSRCS}


INCLUDES = -I$(top_srcdir) \
	-I$(top_srcdir)/src \
	-I$(top_srcdir)/src/libs3decoder \
	-I$(top_srcdir)/src/libutil \
       -I$(top_srcdir)/src/libs3audio \
       -I$(top_srcdir)/src/test/programs/ \
       -I$(top_builddir)/include


LDADD = $(top_builddir)/src/libs3decoder/libs3decoder.la \
	$(top_builddir)/src/libs3audio/libs3audio.la \
	$(top_builddir)/src/libutil/libutil.la \
	-lm @ad_libs@ 



