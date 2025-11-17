from pysubparser import parser
import sys

def replace_words_in_ass(input_file, output_file, replacements):
    """
    Replace specific words in the subtitle text of an ASS file using pysub-parser.
    
    Args:
        input_file (str): Path to the input ASS file.
        output_file (str): Path to save the modified ASS file.
        replacements (dict): Dictionary of words to replace {old_word: new_word}.
    """
    # Read the entire input file to extract metadata
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Extract metadata (everything before the [Events] section)
    metadata = []
    events_header = None
    for line in lines:
        if line.strip().startswith("[Events]"):
            events_header = line  # Save the [Events] header
            break
        metadata.append(line)

    # Extract the Format line under [Events]
    format_line = None
    for line in lines:
        if line.strip().startswith("Format:"):
            format_line = line
            break

    # Parse the subtitles using pysubparser
    subtitles = parser.parse(input_file)

    # Write the modified file
    with open(output_file, "w", encoding="utf-8") as f:
        # Write metadata
        f.writelines(metadata)

        # Write the [Events] header and Format line
        if events_header:
            f.write(events_header)
        if format_line:
            f.write(format_line)

        # Write the modified subtitles
        for subtitle in subtitles:
            new_text = subtitle.text
            for old_word, new_word in replacements.items():
                new_text = new_text.replace(old_word, new_word)
            
            # Ensure the timestamps are in the correct format
            start_time = subtitle.start.strftime("%H:%M:%S.%f")[:-4]  # Trim to 2 decimal places
            end_time = subtitle.end.strftime("%H:%M:%S.%f")[:-4]  # Trim to 2 decimal places

            # Handle missing attributes with default values
            layer = getattr(subtitle, 'layer', 0)  # Default layer is 0
            style = getattr(subtitle, 'style', 'Default')  # Default style is 'Default'
            name = getattr(subtitle, 'name', '')  # Default name is empty
            margin_l = getattr(subtitle, 'margin_l', 0)  # Default margin_l is 0
            margin_r = getattr(subtitle, 'margin_r', 0)  # Default margin_r is 0
            margin_v = getattr(subtitle, 'margin_v', 0)  # Default margin_v is 0
            effect = getattr(subtitle, 'effect', '')  # Default effect is empty

            # Format the subtitle line according to ASS specifications
            text_input = f"Dialogue: {layer},{start_time},{end_time},{style},{name},{margin_l},{margin_r},{margin_v},{effect},{new_text}\n"
            f.write(text_input)

# Example usage
replacements = {
    " لا " : "اذا نحن هنا ؟؟؟ ^__^ " ,
}
replace_words_in_ass('env/test.ass', 'env/output.ass', replacements)