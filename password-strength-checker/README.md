### Password Strength Checker

This project is a Password Strength Checker built using Python and Streamlit. It evaluates the strength of a password based on various criteria such as length, inclusion of uppercase and lowercase letters, digits, and special characters. Additionally, it suggests ways to improve the password strength and provides an option to generate a strong password.

### Deployment
This application is deployed on Streamlit. You can access it [here](https://anas-password-checker.streamlit.app).


## Features
- Checks the strength of a password and provides a score out of 5.
- Gives suggestions to improve the password strength.
- Generates a strong password based on user-specified length.
- Interactive user interface using Streamlit.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/anasahmed07/python-projects.git
   cd python-projects/password-strength-checker
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```sh
   streamlit run main.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the Password Strength Checker.

3. Enter a password to check its strength and receive suggestions to improve it.

4. Use the password generation feature to create a strong password by specifying the desired length.

### Deployment
This application is deployed on Streamlit. You can access it [here](https://anas-password-checker.streamlit.app).

## Example
To check a password's strength:
1. Enter your password in the input field.
2. View the strength rating and suggestions for improvement.

To generate a strong password:
1. Select the desired password length using the slider.
2. Click on "Suggest a Strong Password" to generate a new password.
3. Copy the generated password and store it in a safe place.

## Dependencies
- re
- random
- string
- streamlit

These dependencies are listed in the `requirements.txt` file and can be installed using the provided installation instructions.

## License
This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.