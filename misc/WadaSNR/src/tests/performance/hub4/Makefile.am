INCLUDES = -I$(top_srcdir) \
	-I$(top_srcdir)/src \
	-I$(top_srcdir)/src/libs3decoder \
       -I$(top_srcdir)/src/libs3audio \
       -I$(top_builddir)/include


LDADD = $(top_builddir)/src/libs3decoder/libs3decoder.la \
	$(top_builddir)/src/libs3audio/libs3audio.la \
	$(top_builddir)/src/libutil/libutil.la \
	-lm @ad_libs@ 

HUB4_MODEL_DIR=/lab/speech/sphinx4/data/hub4_model
HUB4_DIR=/lab/speech/sphinx4/data/hub4/eval99/supervised
CTL_FILE=$(HUB4_DIR)/all_hub4.batch
PROGRAMDIR = ${top_builddir}/src/programs
BMBIN = ${top_builddir}/src/test/programs/batchmetrics
LPBIN = $(PROGRAMDIR)/livepretend
DECODEBIN = $(PROGRAMDIR)/decode
ALIGNBIN = /net/elroy/usr1/archan/src/ravi/ALIGN/linux/align 

clean : 
	-rm -f *.ctl *.sent  *.lex *.results *.match *.match.align ARGS.*-{lp,decode}

#all : lp decode
lp :hub4_flatunigram-lp hub4_trigram-lp
decode :hub4_flatunigram-decode hub4_trigram-decode

#hub4_flatunigram-bm hub4_trigram-bm:
#	/bin/cp ARGS.hub4_base ARGS.$@
#	cat ARGS.hub4_base ARGS.hub_base.live ARGS.$(subst -bm,,$@) > ARGS.$@
#	$(BMBIN) $(CTL_FILE) / ./ARGS.$@ > $@.results 


hub4_flatunigram-lp hub4_trigram-lp:
	-rm -f $@.results $@.match $@.match.align
	/bin/cat ARGS.hub4_base ARGS.hub4_base.live ARGS.$(subst -lp,,$@) > ARGS.$@
	awk '{print $$1}' $(CTL_FILE) |sed "s/\.raw//" > ./$@.ctl
	echo "-hyp $@.match" >> ARGS.$@
	$(LPBIN) ./$@.ctl / ./ARGS.$@ > $@.results 2>&1
	awk '{for(i=2;i<=NF;i++){printf("%s ",$$i)}; printf("(%s)\n",$$1)}' $(CTL_FILE) |sed "s/\.raw//" > $@.sent
	tr 'A-Z' 'a-z' < $@.match > $@.tmp
	 - $(ALIGNBIN) -def $@.sent -hyp $@.tmp > $@.match.align

hub4_flatunigram-decode hub4_trigram-decode:
	-rm -f $@.results $@.match $@.match.align
	/bin/cat ARGS.hub4_base ARGS.$(subst -decode,,$@) > ARGS.$@
	awk '{print $$1}' $(CTL_FILE) |sed -e "s/\.raw//" -e "s/supervised/cepstra/"> ./$@.ctl
	echo "-ctl $@.ctl" >> ARGS.$@
	echo "-cepdir / " >> ARGS.$@
	echo "-hyp $@.match" >> ARGS.$@
	$(DECODEBIN) ./ARGS.$@ > $@.results 2>&1 
	awk '{for(i=2;i<=NF;i++){printf("%s ",$$i)}; printf("(%s)\n",$$1)}' $(CTL_FILE) |sed -e "s/\.raw//" -e "s/supervised/cepstra/"> $@.sent
	tr 'A-Z' 'a-z' < $@.match > $@.tmp
	- $(ALIGNBIN) -def $@.sent -hyp $@.tmp > $@.match.align



