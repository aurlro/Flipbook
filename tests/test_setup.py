def test_imports():
    imports = {
        'Flask': 'flask',
        'Flask-WTF': 'flask_wtf',
        'Pillow': 'PIL',
        'PyPDF2': 'PyPDF2',
        'python-dotenv': 'dotenv',
        'pytest': 'pytest'
    }

    results = []
    for name, module in imports.items():
        try:
            __import__(module)
            results.append(f"✅ {name} importé avec succès")
        except ImportError as e:
            results.append(f"❌ {name} NON importé : {str(e)}")

    return results

if __name__ == "__main__":
    print("Test des imports:")
    for result in test_imports():
        print(result)