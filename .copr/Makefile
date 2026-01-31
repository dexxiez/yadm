spec := yadm-dexxiez.spec

# Extract Name/Version from spec to avoid hardcoding
name := $(shell rpmspec -q --qf '%{NAME}\n' $(spec) | head -n1)
ver  := $(shell rpmspec -q --qf '%{VERSION}\n' $(spec) | head -n1)

srpm:
	# Create a tarball with a stable filename and matching topdir
	git archive --format=tar.gz --prefix=$(name)-$(ver)/ \
		-o $(name)-$(ver).tar.gz HEAD
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(PWD)" \
		--define "_specdir $(PWD)" \
		--define "_srcrpmdir $(PWD)"
