yaş = int(input("Yaşınız kaç? "))

if yaş < 18:
    print("yaşınız 18den küçük ehliyet alamazsınız.")
elif yaş == 18:
    print("Ehliyet alabilirsiniz ama dikkatli olun.")
else:
    print("Ehliyet alabilirsiniz.")
