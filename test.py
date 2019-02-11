import random

def __text_to_matrix(text):
        """Converts text to array of strings, filtering out empty lines from result array

        Parameters:
        ----------
        text : str

        Returns:
        ----------
        [str]
        """
        matrix = text.replace('\r', '').split('\n') #filter out \r for Windows environment files
        matrix = [[y for y in x] for x in matrix if x]

        return matrix

number_of_unique_characters = 27
 
def insert_cat(text, pattern, x, y):
    for i in range(0, len(pattern)):
        for j in range(0, len(pattern[i])):
            text[x+i][y+j] = pattern[i][j]
        
n = random.randint(100, 120)
#n = 2
landscape = ''
for i in range(1, n):
    m = random.randint(120, 150)
    for j in range(1, m):
        landscape += chr(ord('a') + random.randint(0, number_of_unique_characters))

    landscape += '\n'

    
landscape = __text_to_matrix(landscape)
landscape = ["*"*(100 + random.randint(5, 10)) for _ in range(0, 65)]
landscape = [[y for y in x] for x in landscape if x]
cat = __text_to_matrix(open("pattern.txt", "r").read())
insert_cat(landscape, cat, 10, 10)
insert_cat(landscape, cat, 10, 80)
insert_cat(landscape, cat, 20, 45)
insert_cat(landscape, cat, 40, 10)
insert_cat(landscape, cat, 40, 80)
text_file = open("Output.txt", "w")
text_file.write("".join(["".join(row) + "\n" for row in landscape]))
text_file.close()
    
print("-------------")  

