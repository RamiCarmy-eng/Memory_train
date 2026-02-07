🧠 Memory Master Pro (English Edition)
Memory Master Pro is an interactive memory training application built in Python. The system helps improve visual and verbal memory through various exercise types, personal progress tracking, and visual feedback.

✨ Key Features
Four Training Modes:

🔵 Shapes: Memorize and identify geometric shapes.

🖼️ Images: Memorize general images from a local directory.

🔢 Numbers: Remember random numeric sequences.

📝 Words: Practice with a personal vocabulary list (my_dictionary.txt).

User Management: Supports multiple users with independent level tracking for each person.

Smart Leveling Engine: * Level Up: Achieve 100% score to advance.

Level Down: Scoring below 50% reduces your level.

Detailed Feedback: Displays exactly what you remembered, what you missed, and any wrong selections.

Improved Input Logic: Case-insensitive word matching and automatic space cleaning for a smoother experience.

🚀 How to Run
Ensure Python 3.x is installed.

Prepare the required asset folders in the same directory as the script:

training_shapes/ (Place shape images here)

training_images/ (Place general images here)

Prepare your vocabulary file:

Create my_dictionary.txt and add words (one word per line).

Note: Using lowercase is recommended.

Install the required library for image processing:

Bash
pip install Pillow
Run the application:

Bash
python main.py
📦 Building the EXE
To create a standalone executable that includes your dictionary and images:

PowerShell
pyinstaller --onefile --windowed `
--add-data "training_shapes;training_shapes" `
--add-data "training_images;training_images" `
--add-data "my_dictionary.txt;." `
--name "MemoryMaster_Pro" `
main.py
🛠️ Technologies
GUI: Tkinter (Standard Python Library).

Image Processing: PIL (Pillow).

Data Storage: JSON (For persistent user progress).

📊 Data Structure
The application stores progress in memory_master_data.json. The keys are now synchronized with the English UI:

JSON
{
    "User_Name": {
        "levels": {
            "Shapes": 5,
            "Images": 3,
            "Numbers": 4,
            "Words": 2
        }
    }
}