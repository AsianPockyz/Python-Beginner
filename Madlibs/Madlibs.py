# # string concatenation (aka how to put strings together)
# # suppose we want to create a string that says "subscribe to ____"
# youtuber = "Asian Pockyz"
# # a few ways of doing this
# print("subscribe to "+ youtuber)
# print("subscribe to {}".format(youtuber))
# # what that does it put youtuber or whatever the value of youtuber is into the curly brackets {}
# # the third method and most straight forward: the f string method
# print(f"subscribe to {youtuber}")

adj = input("Adjective: ")
verb1 = input("Verb: ")
verb2 = input("Verb: ")
famous_person = input ("Famous person: ")

madlib = f"Computer programming is so {adj}! It makes me so excited all the time because \
I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}!"

print(madlib)
