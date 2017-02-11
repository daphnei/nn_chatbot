
all: clean alexa_sample

alexa_sample:
	cp -r ask hello_alexa/ask
	cd hello_alexa; zip -r hello_alexa.zip *
	mv hello_alexa/hello_alexa.zip hello_alexa.zip
	rm -rf hello_alexa/ask

clean:
	rm -f hello_alexa.zip