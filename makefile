# Going crazy with makefiles.

src          = $(wildcard *.py)
flags        = -v -d
test_flags   = -v -d --dry-run
main         = ./main.py
install      = /usr/bin/main.py
soft_install = /usr/sbin/main.py
doc_name     = main_doc
rules        = list ls lint run test_run test package docs install soft_install

ls list:
	$(info Commands:)
	$(foreach rule, $(rules), $(info $(rule)))
	@:  # Shell No-Op

lint:
	flake8 $(src)
	
run:
	$(main) $(flags)
	
test_run:
	$(main) $(test_flags)
	
test:
	@:  # Todo be done.
	
package:
	@:  # Todo be done.
	
docs:
	pandoc -s readme.md -o $(doc_name)
	
install:
	cp -f -r $(realpath $(main)) $(install)
	
soft_install:
	ln -f -s $(realpath $(main)) $(soft_install)
