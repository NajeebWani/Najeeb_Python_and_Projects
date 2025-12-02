class Design_Pattern:

    # Seedha  triangle
    def triangle_design(self):
        rows = 5        #Total no of rows
        i = 1           #row counter start from 1
        while i <= rows:   #loop
            space = 1       #print spaces
            while space <= rows - i: #spaces decrease as rows increase
                print(" ", end="")   #print spaces without new line
                space += 1     
            star = 1
            while star <= i:         #stars increase as rows increase
                print("* ", end="")   #print star with a new space
                star += 1
            print()  # move cursor to next line after each row
            i += 1    # go to nxt row

    # Ulta  triangle
    def reverse_triangle(self):
        rows = 5        # total no of rows
        i = rows         # row counter start from last row
        while i >= 1:    #loop until row 1
            space = 1
            while space <= rows - i:   #space increase as row decrease
                print(" ", end="")
                space += 1
            star = 1
            while star <= i:   #stars decrease as rows decrease
                print("* ", end="")
                star += 1
            print()        # move cursor to nxt line
            i -= 1     # go to previous row


# Object create
myobj = Design_Pattern()

print("Seedha Triangle:")
myobj.triangle_design()

print("\nUlta Triangle:")
myobj.reverse_triangle()
