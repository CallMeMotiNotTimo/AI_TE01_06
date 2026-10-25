import finders

item_list=["A game of thrones","A clash of kings","A storm of swords",
           "After Many a Summer Dies the Swan",
           "By Grand Central Station I Sat Down and Wept",
           "Cabbages and Kings","Dance Dance Dance","A Dance With Dragons","A game thrones"]
keyword=input("Enter the keyword:")
print(finders
      .element_finder(item_list,keyword))
