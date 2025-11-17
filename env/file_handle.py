import ass 
import sys
def printer() : 
  

  sys.stdout.reconfigure(encoding='utf-8')

  with open("D:/python learning/file_handling_python/env/test.ass", encoding='utf_8_sig') as f:
     
     doc = ass.parse(f)

     if not doc.events:

        print("No subtitle events found.")

        return None
     
     text = doc.events


     print(text)

     return text
  
whatever = printer()

