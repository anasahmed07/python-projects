# Unit Converter

This repository contains a unit converter application built using Streamlit. The application allows users to convert values between different units across various categories such as Length, Mass, Temperature, Area, Volume, Time, Speed, Pressure, Energy, Frequency, Digital Storage, Data Transfer Rate, Fuel Economy, and Plane Angle.

Try it out here: [Unit Converter App](https://anas-unit-converter.streamlit.app/)

## Features

- Converts values between various units across multiple categories.
- Simple and intuitive user interface built with Streamlit.
- Supports a wide range of units and categories.

## Installation

To run the unit converter application, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/anasahmed07/unit-convertor.git
    cd unit-convertor
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit application**:
    ```bash
    streamlit run main.py
    ```

## Usage

1. Open your web browser and go to `http://localhost:8501` to access the unit converter application.
2. Select the category of units you want to convert.
3. Choose the units for conversion (from and to).
4. Enter the value you want to convert.
5. The converted value will be displayed automatically.

## Categories and Units

The application supports a wide range of units across various categories:

- **Length**: Kilometre, Metre, Centimetre, Millimetre, Micrometre, Nanometre, Mile, Yard, Foot, Inch, Nautical Mile
- **Mass**: Kilogram, Gram, Milligram, Pound, Ounce
- **Temperature**: Celsius, Fahrenheit, Kelvin
- **Area**: Square Kilometre, Square Metre, Square Centimetre, Square Millimetre, Hectare, Acre
- **Volume**: Cubic Metre, Litre, Millilitre, Cubic Centimetre, Cubic Inch, Cubic Foot
- **Time**: Second, Minute, Hour, Day
- **Speed**: Metre per second, Kilometre per hour, Mile per hour, Knot
- **Pressure**: Pascal, Bar, PSI, Atmosphere
- **Energy**: Joule, Kilojoule, Calorie, Kilocalorie, Watt-hour, Kilowatt-hour
- **Frequency**: Hertz, Kilohertz, Megahertz, Gigahertz
- **Digital Storage**: Bit, Byte, Kilobyte, Megabyte, Gigabyte, Terabyte
- **Data Transfer Rate**: Bit per second, Kilobit per second, Megabit per second, Gigabit per second, Terabit per second
- **Fuel Economy**: Miles per gallon, Litres per 100 km
- **Plane Angle**: Degree, Radian

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Streamlit for providing an easy-to-use framework for building web applications in Python.
