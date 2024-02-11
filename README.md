# Yggdrasil


This project implements a Streamlit-based chatbot interface that integrates with OpenAI's GPT-3 and GPT-4 models. It provides a dynamic, interactive chat experience by leveraging Streamlit for the web interface and OpenAI's API for generating chat responses. The application also includes file handling for user profiles and persona customization.

## Features

- **Dynamic Chat Interface**: Utilizes Streamlit for an interactive chat interface.
- **GPT-3 and GPT-4 Integration**: Supports chatting with both GPT-3 and GPT-4 models.
- **User Profile Management**: Manages user profiles stored in text files for personalized experiences.
- **Persona Customization**: Allows the customization of chatbot personas through text files.
- **Environment Variable Management**: Uses `.env` files for secure API key storage.

## Setup

1. **Install Dependencies**: Ensure you have Python installed, then install the required packages using pip:

```bash
pip install streamlit dotenv openai pillow
```

2. **Environment Variables**: Edit the `env.template` file at the root of your project directory and add your OpenAI API key:

```plaintext
OPENAI_API_KEY='your_api_key_here'
```
Then save file as .env

3. **Running the Application**: Start the application by running:

```bash
streamlit run app.py
```

## Usage

- **Starting the Chat**: Once the application is running, interact with the chatbot through the Streamlit interface.
- **User Profile and Persona**: The application automatically manages user profiles.
- **Dynamic Response Generation**: Chat responses are generated dynamically, simulating a conversational flow with artificial delay for each word.

## Customization

- **Profile and Persona Files**: Customize the chatbot's persona and user profiles by modifying the respective markdown files in the `Personas` and `Memories` directories.
- **Avatar Customization**: You can change the chatbot's avatar by replacing the `Emily.png` image in the `Portrait` directory.

## Important Functions

- `ensure_userprofile_exists(filepath)`: Ensures the user profile file exists, creating it if necessary.
- `open_file(filepath)`: Opens and reads the content of a given file.
- `chatbotGPT4(conversation, model, temperature, max_tokens)`: Sends a conversation to the GPT-4 model and returns the response.
- `chatbotGPT3(conversation, model, temperature, max_tokens)`: Similar to `chatbotGPT4`, but uses the GPT-3 model.
- `response_generator(msg_content)`: Simulates dynamic response generation with an artificial delay.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to suggest improvements or add new features.

## License

MIT LICENCE

---
**Note**: This README is a guide to get started with the Streamlit Chatbot Interface. Adjust the setup and customization instructions as needed for your specific use case.
```
