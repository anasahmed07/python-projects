import streamlit as st

def convert_units(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {
            "Kilometre": 1000,
            "Metre": 1,
            "Centimetre": 0.01,
            "Millimetre": 0.001,
            "Micrometre": 1e-6,
            "Nanometre": 1e-9,
            "Mile": 1609.34,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254,
            "Nautical Mile": 1852
        },
        "Mass": {
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 1e-6,
            "Pound": 0.453592,
            "Ounce": 0.0283495
        },
        "Temperature": {
            "Celsius": lambda x: x,
            "Fahrenheit": lambda x: (x - 32) * 5/9,
            "Kelvin": lambda x: x - 273.15
        },
        "Area": {
            "Square Kilometre": 1e6,
            "Square Metre": 1,
            "Square Centimetre": 0.0001,
            "Square Millimetre": 1e-6,
            "Hectare": 10000,
            "Acre": 4046.86
        },
        "Volume": {
            "Cubic Metre": 1,
            "Litre": 0.001,
            "Millilitre": 1e-6,
            "Cubic Centimetre": 1e-6,
            "Cubic Inch": 1.63871e-5,
            "Cubic Foot": 0.0283168
        },
        "Time": {
            "Second": 1,
            "Minute": 60,
            "Hour": 3600,
            "Day": 86400
        },
        "Speed": {
            "Metre per second": 1,
            "Kilometre per hour": 0.277778,
            "Mile per hour": 0.44704,
            "Knot": 0.514444
        },
        "Pressure": {
            "Pascal": 1,
            "Bar": 100000,
            "PSI": 6894.76,
            "Atmosphere": 101325
        },
        "Energy": {
            "Joule": 1,
            "Kilojoule": 1000,
            "Calorie": 4.184,
            "Kilocalorie": 4184,
            "Watt-hour": 3600,
            "Kilowatt-hour": 3.6e6
        },
        "Frequency": {
            "Hertz": 1,
            "Kilohertz": 1000,
            "Megahertz": 1e6,
            "Gigahertz": 1e9
        },
        "Digital Storage": {
            "Bit": 1,
            "Byte": 8,
            "Kilobyte": 8192,
            "Megabyte": 8.38861e6,
            "Gigabyte": 8.58993e9,
            "Terabyte": 8.79609e12
        },
        "Data Transfer Rate": {
            "Bit per second": 1,
            "Kilobit per second": 1000,
            "Megabit per second": 1e6,
            "Gigabit per second": 1e9,
            "Terabit per second": 1e12
        },
        "Fuel Economy": {
            "Miles per gallon": 1,
            "Litres per 100 km": lambda x: 235.215 / x
        },
        "Plane Angle": {
            "Degree": 1,
            "Radian": 57.2958
        }
    }
    
    if category not in conversion_factors:
        return None
    
    if from_unit not in conversion_factors[category] or to_unit not in conversion_factors[category]:
        return None
    
    if category == "Temperature":
        value_in_celsius = conversion_factors[category][from_unit](value)
        if to_unit == "Celsius":
            return value_in_celsius
        elif to_unit == "Fahrenheit":
            return value_in_celsius * 9/5 + 32
        elif to_unit == "Kelvin":
            return value_in_celsius + 273.15
    elif category == "Fuel Economy" and from_unit == "Miles per gallon" and to_unit == "Litres per 100 km":
        return conversion_factors[category][to_unit](value)
    elif category == "Fuel Economy" and from_unit == "Litres per 100 km" and to_unit == "Miles per gallon":
        return 235.215 / value
    else:
        value_in_base = value * conversion_factors[category][from_unit]
        converted_value = value_in_base / conversion_factors[category][to_unit]
        return converted_value


categories = [
    "Length", "Mass", "Temperature", "Area", "Volume", "Time", "Speed", 
    "Pressure", "Energy", "Frequency", "Digital Storage", "Data Transfer Rate", 
    "Fuel Economy", "Plane Angle"
]

units = {
    "Length": ["Kilometre", "Metre", "Centimetre", "Millimetre", "Micrometre", "Nanometre", "Mile", "Yard", "Foot", "Inch", "Nautical Mile"],
    "Mass": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Area": ["Square Kilometre", "Square Metre", "Square Centimetre", "Square Millimetre", "Hectare", "Acre"],
    "Volume": ["Cubic Metre", "Litre", "Millilitre", "Cubic Centimetre", "Cubic Inch", "Cubic Foot"],
    "Time": ["Second", "Minute", "Hour", "Day"],
    "Speed": ["Metre per second", "Kilometre per hour", "Mile per hour", "Knot"],
    "Pressure": ["Pascal", "Bar", "PSI", "Atmosphere"],
    "Energy": ["Joule", "Kilojoule", "Calorie", "Kilocalorie", "Watt-hour", "Kilowatt-hour"],
    "Frequency": ["Hertz", "Kilohertz", "Megahertz", "Gigahertz"],
    "Digital Storage": ["Bit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"],
    "Data Transfer Rate": ["Bit per second", "Kilobit per second", "Megabit per second", "Gigabit per second", "Terabit per second"],
    "Fuel Economy": ["Miles per gallon", "Litres per 100 km"],
    "Plane Angle": ["Degree", "Radian"]
}

with st.container(border=True):
    st.title("Unit Converter")
    category = st.selectbox("Select Category:", categories, key="category")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            from_unit = st.selectbox("From Unit:", units[category], key="from_unit")
            value = st.number_input("Enter value:", format="%f", key="value")

        with col2:
            to_unit = st.selectbox("To Unit:", units[category], key="to_unit")
            converted_value = convert_units(value, from_unit, to_unit, category)
            st.number_input("Converted value:", value=converted_value if from_unit != to_unit else value, format="%f", key="converted_value", disabled=True)