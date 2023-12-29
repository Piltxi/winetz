from language_tool_python import LanguageTool


def initCorrectionTool():
    tool = LanguageTool('it-IT')
    return tool

def maybeMeaning (text, tool):
    # Correzione ortografica
    text = 'Il testo con errori.'
    matches = tool.check(text)

    # Stampa suggerimenti
    print(matches)