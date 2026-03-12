# LanguageTool Setup Guide

Your VS Code workspace is already configured for LanguageTool grammar checking. You just need to start the local server.

## Option 1: Using Docker (Easiest)

```bash
docker run -d -p 8081:8081 erikvl87/languagetool
```

Then your VS Code grammar checker will automatically connect.

## Option 2: Manual Java Setup

1. **Download LanguageTool**:
   - Visit: https://github.com/languagetool-org/languagetool/releases
   - Download the latest `LanguageTool-X.X-stable.zip` (standalone)
   - Extract it to: `/Users/eliabluvanda/econometrics_notes/tools/`

2. **Start the Server**:
   ```bash
   cd /Users/eliabluvanda/econometrics_notes/tools/LanguageTool-*/
   java -jar languagetool-server.jar --port 8081
   ```

3. **Verify it's running**:
   ```bash
   curl http://localhost:8081
   ```
   You should see HTML output.

## Option 3: Use the Startup Script

Once LanguageTool is downloaded to `tools/`, run:
```bash
./start-languagetool.sh
```

## After Starting the Server

1. Open any `.qmd`, `.md`, or `.tex` file in VS Code
2. Grammar and spelling suggestions will appear as red/blue underlines
3. Hover over them to see recommendations

## Configuration

Your workspace settings are in `.vscode/settings.json`:
- Language: en-US
- Server: http://localhost:8081
- Supports: Markdown, LaTeX, Quarto, Plain Text

## Troubleshooting

- **Port 8081 in use?** Kill it with: `lsof -ti:8081 | xargs kill -9`
- **Java not found?** Install with: `brew install openjdk@17`
- **Server not responding?** Check: `curl http://localhost:8081/v2/languages`
