This is a demo project for a chatbot that answers crypto questions using AI + my context(an API call to cryptopanic fetching news data).

This is a demo project, the context can be a dedicated knowledge base to your own company documents etc.

It uses **LangChain**, **Faiss** (vector DB), and **OpenAI** to fetch relevant crypto info
and provide intelligent answers.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/crypto-qa-chatbot.git
```

2. Install the dependencies:
   I use uv as a development server, you can use any other server of your choice.

```bash
uv init
```

3. Run the application:

```bash
uv run main.py
```

## Usage

1. Ask the bot any question about crypto.
2. The bot will provide an answer based on the context it has.
3. The context is updated every time you refresh the page.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.
