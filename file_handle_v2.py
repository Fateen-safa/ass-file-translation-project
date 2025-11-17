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
    # Parse the ASS file
    sys.stdout.reconfigure(encoding='utf-8')

    subtitles = parser.parse(input_file)

    modified_subtitles = []
    with open(output_file, "w", encoding="utf-8") as f:
    # Iterate over each subtitle and replace words
       for subtitle in subtitles:
         new_text = subtitle.text
         for old_word, new_word in replacements.items():
              new_text = new_text.replace(old_word, new_word)
              ##text_input = f"  {subtitle.start} --> {subtitle.end}\n{new_text}\n\n"
              text_input = f"Dialogue:{subtitle.start},{subtitle.end},Italics,,0,0,0,,{new_text}\n"
              print(new_text)
              f.write( text_input )
 
        
        

    # Save the modified subtitles to a new file

# Example usage
replacements = {
    "تجلب": "بتثتسنمبتسنيتبينتمنبتسمنتبنعم",
}
replace_words_in_ass('env/test.ass', 'env/output.ass', replacements) 

