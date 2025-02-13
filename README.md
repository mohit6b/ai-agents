# ai-agents
# Food Ordering Assistant

This repository contains 2 AI-Agents:
1. Telegram Auto-responder fro lunch planning with friends - a python script that enables telegram to respond automatically
2. Order food based on the user prompts - full-stack application featuring a React frontend with a Flask backend that simulates a food ordering workflow. experience.

## Features

- Interactive chat interface
- Step-by-step food ordering process
- Real-time responses
- Persistent user sessions

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip (Python package manager)

## Project Structure

```
ai-agents/
├── frontend/          # React frontend
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── src
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── tailwind.config.js
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── backend/          
    ├── telegram_auto-responder.py   # pythin script
    └── order_food_ai_agent.py    # Flask backend
```

## Setup Instructions

### Backend Setup

1. Make sure that npm, python3 and pip3 are installed.

2. Install Python dependencies:
   ```bash
   pip3 install <<PACKAGE_NAME>>
   ```

3. Start the Flask server/Python Script for the food order. Before running telegram auto-responder script please make sure env variables are set properly:
   ```bash
   TELEGRAM_API_ID=<<ENTER_YOUR_TELEGRAM_API_ID>>
   TELEGRAM_API_HASH=<<ENTER_YOUR_TELEGRAM_API_HASH>>
   ```

   ```bash
   python3 order_food_ai_agent.py
   python3 telegram_auto-responder.py
   ```

The backend server will start running at `http://localhost:5002`.

### Frontend Setup

1. Install Node.js dependencies. Make sure you are inside frontend repositoty:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend development server will start and open in your default browser.

## Usage

1. Open your browser and navigate to the frontend URL (`http://localhost:5173`)
2. The chat interface will automatically greet you
3. Follow the prompts to:
   - Select your food
   - Provide delivery address
   - Enter payment details
   - Confirm your order

Key files:
- `frontend/src/App.tsx`: Frontend main application component
- `frontend/src/main.tsx`: Frontend application entry point
- `frontend/src/index.css`: Frontend Global styles
- `backend/telegram_auto-responder.py`: Python script for telegram auto-responder
- `backend/order_food_ai_agent.py`: Flask server for food order agent


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
