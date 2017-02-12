
all: clean alexa_sample chatbot

alexa_sample:
	cp -r ask hello_alexa/ask
	cd hello_alexa; zip -r hello_alexa.zip *
	mv hello_alexa/hello_alexa.zip hello_alexa.zip
	rm -rf hello_alexa/ask

chatbot:
	cp -r ask alexa_chatbot/ask
	cd alexa_chatbot; zip -r alexa_chatbot.zip *
	mv alexa_chatbot/alexa_chatbot.zip alexa_chatbot.zip
	rm -rf alexa_chatbot/ask

clean:
	rm -f hello_alexa.zip
	rm -f alexa_chatbot.zip