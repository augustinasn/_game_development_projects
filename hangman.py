# Import prerequisites:

from random import randint
from sys import exit

#Define and assign variables:

words_list = {"namas":"objektas", 
              "šuo":"gyvūnas", 
              "katė":"gyvūnas",
              "stalas":"objektas",
              "vilnius":"miestas",
              "trakai":"miestas",
              "papūga":"gyvūnas",
              "televizorius":"buities prietaisas"}
lives = 5
score = 0
guess = "placeholder"
hint = "placeholder"
used_guesses = []

#Initialization:

secret_word = list(words_list.keys())[randint(1, len(words_list)) - 1]
hint = words_list[secret_word]
secret_word_to_list = list(secret_word)
display_seq = list(map(lambda x : "_", secret_word_to_list))

#Define funcions:

def print_line():
  print("************")  

def print_info():
  print_line()
  print("Jums pateiktas žodis:")
  print(" . ".join(display_seq))
  print_line()  
  print("Užuomena - tai yra", hint)
  print_line()
  print("Gyvybių likutis:", lives)
  print("Jūsų rezultatas:", score, "%")
  print_line()
  
def guess_char():
  global lives
  global used_guesses
 
  if guess in used_guesses:
    print_line()    
    print("Jau spėjote", guess, "ankčiau! Bandykite dar.")
    return
  
  if guess.isalpha() == False:
    print_line()
    print("Spėjimas turi būti raidė!")
    return

  if len(guess) != 1:
    print_line()
    print("Spėjimą turėtų sudaryti tik vienas simbolis!")
    return

  if guess in secret_word_to_list:
    used_guesses.append(guess)
    for i in range(len(secret_word_to_list)):
      if secret_word_to_list[i] == guess:
        display_seq[i] = guess

  else:
    lives = lives - 1
    print("Raidės", guess, "jums pateiktame žodyje nėra...")
    used_guesses.append(guess)
    
def count_score():
  return ((len(secret_word) - display_seq.count("_")) / len(secret_word)) * 100

def check_score():
  global score
  global lives
  
  score = count_score()
  
  if score == 100:
    print("Sveikiname! Jūs atspėjote jums pateiktą žodį, jis buvo -", secret_word)
    exit()
    
  if lives == 0:
    print("Užjaučiame, sunaudojote visas gyvybes neatspėję jums priskirto žodžio, kuris buvo -", secret_word)     
    exit()

#Runtime:

print("Sveiki atvykę į Pakaruoklio žaidimą!")
print("Jūsų tikslas atspėti jums pateiktą žodį neišnaudojant suteiktų (5) gyvybių.")
print_info()

while lives > 0:
  guess = input("Spėkite raidę: ")
  guess_char()
  check_score()
  print_info()
  print("\n")

  
 