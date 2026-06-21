# ProposalAI

**AI Proposal Generator** — turn freelance job postings into complete, client-ready proposal packages in seconds.

ProposalAI is a Flask web application that analyzes job descriptions using the Groq API and generates structured outputs freelancers need to respond quickly and professionally: scope summary, complexity rating, budget and timeline estimates, a polished proposal draft, and clarifying questions for the client.

---

## Features

- **Instant proposal generation** — paste a job description and receive a full analysis package
- **Six AI-generated outputs**
  - Project summary
  - Complexity score (1–10)
  - Estimated budget range
  - Estimated timeline
  - Professional proposal letter
  - Questions for the client
- **Copy tools** — copy the proposal alone or the entire analysis with one click
- **Analysis history** — last 10 analyses saved locally to `history.json`
- **History sidebar** — browse and reload previous results instantly
- **Premium UI** — modern dark theme with gradients, glass cards, and responsive layout
- **Mobile-friendly** — collapsible history sidebar and adaptive layout for all screen sizes

---

## Technologies Used

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| AI | Groq API (`llama-3.3-70b-versatile`) |
| Frontend | HTML, CSS, JavaScript |
| Config | python-dotenv |
| Storage | Local JSON file (`history.json`) |

---

## Installation

### Prerequisites

- Python 3.10+ (compatible with Python 3.14)
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-proposal-generator.git
cd ai-proposal-generator
```

### 2. Create a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Or set it in your shell:

```powershell
# Windows
$env:GROQ_API_KEY = "gsk_your_groq_api_key_here"
```

```bash
# macOS / Linux
export GROQ_API_KEY="gsk_your_groq_api_key_here"
```

---

## Usage

### Start the server

```bash
python app.py
```

Open your browser at:

```
http://127.0.0.1:5000
```

### Generate a proposal

1. Paste a freelance job description into the text area
2. Click **Generate Proposal**
3. Review the analysis cards and proposal package
4. Use **Copy Proposal** or **Copy Everything** to copy content to your clipboard
5. Open the **History** sidebar (mobile) or use the left panel (desktop) to reload past analyses

### Project structure

```
ai-proposal-generator/
├── app.py              # Flask backend and API routes
├── requirements.txt    # Python dependencies
├── history.json        # Saved analysis history (auto-created)
├── templates/
│   └── index.html      # Main UI
└── static/
    └── style.css       # Styles
```

---

## Screenshots

> Add screenshots to `docs/screenshots/` and update the paths below before publishing to GitHub.

### Home

![ProposalAI home screen — job description input and generate button](docs/screenshots/home.png)

### Results

![Generated proposal package with metrics, summary, and proposal draft](docs/screenshots/results.png)

### History sidebar

![Analysis history sidebar showing saved proposals](docs/screenshots/history.png)

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Main web interface |
| `POST` | `/generate` | Generate a proposal from a job description |
| `GET` | `/history` | List the last 10 saved analyses |
| `GET` | `/history/<id>` | Retrieve a specific saved analysis |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for AI generation |

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.
