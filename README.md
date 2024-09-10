# Password-Finder-CTF
Cool tool for CTF automation (still in progress)

# 🔍 Password Finder

A powerful and efficient Python script to recursively scan directories and identify potential passwords in various file types.

## 🚀 Features

- Recursively scans directories for target file types (.txt, .config, .conf, .env)
- Uses multi-processing for improved performance
- Identifies potential passwords based on specific criteria
- Skips large files (>10MB) and certain directories (e.g., OneDrive)
- Handles text encoding and permission errors gracefully

## 🛠️ Installation

1. Clone this repository:
   ```
   git clone https://github.com/0xCZR1/Password-Finder-CTF.git
   ```
2. Navigate to the project directory:
   ```
   cd Password-Finder-CTF
   ```
3. No additional dependencies required! This script uses Python's standard library.

## 🖥️ Usage

Run the script from the command line:

```
python password_finder.py
```

When prompted, enter the directory path you want to scan.

## 🧠 How it works

1. The script recursively scans the provided directory for target file types.
2. It reads the content of each file, ignoring binary files and handling encoding errors.
3. The content is analyzed to identify potential passwords based on criteria such as:
   - Length (8-20 characters)
   - Presence of lowercase and uppercase letters
   - Presence of digits and symbols
   - Exclusion of common programming patterns (e.g., variable declarations)
4. Results are printed to the console, showing the file path and potential passwords found.

## ⚠️ Disclaimer

This tool is for educational and security auditing purposes only. Always ensure you have the necessary permissions before scanning files or systems. The authors are not responsible for any misuse or damage caused by this script.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/0xCZR1/Password-Finder-CTF/issues).

## 📝 License

This project is [MIT]((https://github.com/0xCZR1/Password-Finder-CTF/blob/main/LICENSE)) licensed.

## 🙋‍♂️ Author

Your Name
- GitHub: [@0xCZR](https://github.com/0xCZR1)
- LinkedIn: [Cezar Branduse](https://linkedin.com/in/cezar-branduse-b72445159/)

---

Remember to star ⭐ this repo if you find it helpful!
