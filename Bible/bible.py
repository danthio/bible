import json
import tkinter as tk
import math
from PIL import Image,ImageTk,ImageDraw
from tkinter import font
import re
import time


"""
im=Image.open("data/bg.png")
x,y=im.size
im=im.resize((1000,int(1000*y/x)))
x,y=im.size
yy=int((y-600)/2)
im=im.crop((0,yy,x,y-yy))
im.save("data/bg.png")


def darken_image(image_path, output_path, opacity=0.5):

    # Open the original image
    img = Image.open(image_path).convert("RGBA")
    
    # Create a black overlay with the same size as the image
    black_overlay = Image.new("RGBA", img.size, (0, 0, 0, int(255 * opacity)))
    
    # Composite the black overlay onto the image
    darkened_img = Image.alpha_composite(img, black_overlay)
    
    # Save the result
    darkened_img.save(output_path)

# Example usage

darken_image("data/bg.png", "data/bg2.png", opacity=0.55)"""

niv={}
kjv={}


try:

    with open("data/KJV_bible.json", "r") as file:
        kjv = json.load(file)


except:
    pass




try:

    with open("data/NIV_bible.json", "r") as file:
        niv = json.load(file)


except:
    pass






books=[]
books2=[]

for i in niv:
	books.append(i)


def hex_to_rgba(hex_color, alpha):
    """Convert hex color like '#ff1f83' to RGBA tuple."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b, int(alpha * 255))

images=[]
def create_polygon(*args, **kwargs):
    global can,images





    if "alpha" in kwargs:         
        if "fill" in kwargs:
            # Get and process the input data
            c=kwargs.pop("can")
            outline = kwargs.pop("outline") if "outline" in kwargs else None

            # We need to find a rectangle the polygon is inscribed in
            # (max(args[::2]), max(args[1::2])) are x and y of the bottom right point of this rectangle
            # and they also are the width and height of it respectively (the image will be inserted into
            # (0, 0) coords for simplicity)
            image = Image.new("RGBA", (max(args[::2]), max(args[1::2])))

            fill=hex_to_rgba(kwargs.pop("fill"), kwargs.pop("alpha"))

            ImageDraw.Draw(image).polygon(args, fill=fill, outline=outline)



            images.append(ImageTk.PhotoImage(image))  # prevent the Image from being garbage-collected


            return c.create_image(0, 0, image=images[-1], anchor="nw")  # insert the Image to the 0, 0 coords





def can2_b3(e):
	global ar_h
	global state

	for i in ar_h:


		if i[1]<=can2.canvasy(e.y)<=i[2]:

			highlights_(i[0])

			if state=="main":
				main()
			elif state=="view_highlights":
				view_highlights()

			return
ar_h=[]
def view_highlights():
	global w,h
	global state
	global can1,can2
	global book_
	global ar_h
	global sb_sz
	global back
	global bg2,bg_

	state="view_highlights"

	can1.delete("all")
	can2.delete("all")


	can1.create_image(0,0,image=bg2,anchor="nw")

	bg_=can2.create_image(-2.5,can2.canvasy(-50),image=bg2,anchor="nw")




	can1.create_text(w/2,25,text="Highlights",font=("FreeMono",20),fill="#ffffff")
	can1.create_image(w-5-30,5,image=back,anchor="nw")




	can1.create_text(10,h-25,text=book_,font=("FreeMono",13),fill="#ff1f83",anchor="w")

	#try:

	with open("data/highlights.json", "r") as file:
	    h_ = json.load(file)


	_h_=sorted(h_.items())

	ar=[]


	for i in _h_:

		ar.append(i)




	if len(ar)==0:

		can2.create_text(int(can2["width"])/2,int(can2["height"])/2,
			text="No Record",font=("FreeMono",20),fill="#ff1f83")



	def count_newlines(text):
	    return len(re.findall(r'\n', text))


	_y=20

	ar_h=[]



	for i in ar:

		
		i2=i[1][book_].split(" ")

		y1=_y

		can2.create_text(5,_y,text=i[0],font=("FreeMono",13),fill="#ffffff",anchor="nw")

		_y+=30


		txt=str(i[0].split(" ")[1].split(":")[1])+" "
		txt2=txt

		sz=int(can2["width"])-sb_sz-50

		x=5
		for _ in range(len(i2)):

			#print(txt2)

			try:


				

				if get_text_length(can2, txt2+i2[_+1]+" ", "FreeMono", 13)<=sz:
					txt+=i2[_]+" "
					txt2+=i2[_]+" "
				else:
					txt+="\n"+i2[_]+" "
					txt2="\n"+i2[_]+" "
			except:
				txt+=i2[_]+" "






		can2.create_text(5,_y,text=txt,anchor="nw",font=("FreeMono",13),fill="#ff1f83")


		#print(txt)


		nl=count_newlines(txt)

		if nl==0:
			nl=1



		_y+=nl*30


		y2=_y

		ar_h.append([i[0],y1,y2])

		_y+=30





	_y+=10


	

	if _y>int(can2["height"]):
		can2["scrollregion"]=(0,0,int(can2["width"]),_y)
	else:
		can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))

	can2.place(in_=root,x=2.5,y=50)


	draw_sb()

	#except:
	#	pass


def highlights_(v):
	global niv,kjv




	try:

	    with open("data/highlights.json", "r") as file:
	        h_ = json.load(file)


	except:
	    h_={}


	
	try:


		v_=h_[v]   

		h_.pop(v)

	except:

		b=v.split(" ")[0]
		c=v.split(" ")[1].split(":")[0]
		ve=v.split(" ")[1].split(":")[1]


		h_[v]={"NIV":niv[b][c][ve],"KJV":kjv[b][c][ve]}


	with open("data/highlights.json", "w") as file:
	    json.dump(h_, file, indent=4)







def save(v):



	save_={"save":[]}
	save_["save"]=v	   


	with open("data/save.json", "w") as file:
	    json.dump(save_, file, indent=4)
def get_text_length(canvas, text, font_name, font_size):
    # Create a tkinter font object with the given font name and size
    text_font = font.Font(family=font_name, size=font_size)

    # Measure the width of the text in pixels
    text_width = text_font.measure(text)
    return text_width

#print(len(niv["Genesis"]["2"]))
ar_h=[]
def main():
	global w,h
	global can1,can2 
	global state
	global sel_book,sel_chapter,sel_verse
	global book
	global sb_sz
	global ar_h
	global previous,next_
	global sb_h
	global book_
	global bg2,bg_


	highlighted=[]

	try:

	    with open("data/highlights.json", "r") as file:
	        h_ = json.load(file)


	    for i in h_:
	    	highlighted.append(i)
	except:
		pass


	state="main"


	if book_=="NIV":
		book=niv
	if book_=="KJV":
		book=kjv


	ar=[]
	ar_h=[]

	if sel_verse==0:

		if sel_chapter==0:


			n=len(book[sel_book]["1"])
			c=1

			for _ in range(n):
					
				ar.append([book[sel_book]["1"][str(c)],sel_book+" 1:"+str(c)])

				c+=1


		else:


			n=len(book[sel_book][str(sel_chapter)])
			c=1

			for _ in range(n):
					
				ar.append([book[sel_book][str(sel_chapter)][str(c)],sel_book+" "+str(sel_chapter)+":"+str(c)])

				c+=1
	else:
		ar.append([book[sel_book][str(sel_chapter)][str(sel_verse)],sel_book+" "+str(sel_chapter)+":"+str(sel_verse)])



	can1.delete("all")
	can2.delete("all")


	can1.create_image(0,0,image=bg2,anchor="nw")

	bg_=can2.create_image(-2.5,can2.canvasy(-50),image=bg2,anchor="nw")



	if sel_chapter==0:

		title=sel_book+" 1"
		sel_chapter=1
	else:

		if not sel_verse==0:

			title=sel_book+" "+str(sel_chapter)+" : "+str(sel_verse)
		else:
			title=sel_book+" "+str(sel_chapter)




	can1.create_text(w/2,25,text=title,font=("FreeMono",20),fill="#ffffff")


	can1.create_image(w-30-5,5,image=back,anchor="nw")

	xx=int(can2["width"])/3


	can1.create_text(10,h-25,text=book_,font=("FreeMono",13),fill="#ff1f83",anchor="w")
	can1.create_image(xx-15,h-50+(50-30)/2,image=previous,anchor="nw")
	can1.create_image(int(can2["width"])-xx-15,h-50+(50-30)/2,image=next_,anchor="nw")

	can1.create_text(int(can2["width"])/2,h-25,text=str(sel_chapter)+"/"+
		str(len(book[sel_book])),font=("FreeMono",13),fill="#ff1f83")





	def count_newlines(text):
	    return len(re.findall(r'\n', text))


	_y=20
	c=1

	for i in ar:

		
		i2=i[0].split(" ")

		y1=_y

		if sel_verse!=0:

			txt=str(sel_verse)+" "
			txt2=str(sel_verse)+" "

		else:
			txt=str(c)+" "
			txt2=str(c)+" "

		sz=int(can2["width"])-sb_sz-50

		x=5
		for _ in range(len(i2)):

			#print(txt2)

			try:


				

				if get_text_length(can2, txt2+i2[_+1]+" ", "FreeMono", 13)<=sz:
					txt+=i2[_]+" "
					txt2+=i2[_]+" "
				else:
					txt+="\n"+i2[_]+" "
					txt2="\n"+i2[_]+" "
			except:
				txt+=i2[_]+" "




		col="#ffffff"

		try:
			v=highlighted.index(i[1])
			col="#ff1f83"
		except:
			pass


		can2.create_text(5,_y,text=txt,anchor="nw",font=("FreeMono",13),fill=col)


		#print(txt)


		nl=count_newlines(txt)

		if nl==0:
			nl=1



		_y+=nl*30


		y2=_y

		ar_h.append([i[1],y1,y2])

		_y+=30


		c+=1



	_y+=10


	

	if _y>int(can2["height"]):
		can2["scrollregion"]=(0,0,int(can2["width"]),_y)

	can2.place(in_=root,x=2.5,y=50)


	draw_sb()


	







def can2_b1(e):

	global state
	global w,h
	global can1,can2
	global books3,sel_book
	global sel_chapter
	global sel_verse,verses

	global sb_sz,sb_col,sb_h,sb_st

	if (int(can2["width"])-sb_sz-1)<=e.x<=(int(can2["width"])):

	    sb_st=1


	    h_=int(can2["height"])/int(can2["scrollregion"].split(" ")[-1])*int(can2["height"])

	    if not e.y+h_>int(can2["height"]):
	        sb_move(e.y,e.y*int(can2["scrollregion"].split(" ")[-1])/int(can2["height"]))
	    else:
	        sb_move(int(can2["height"])-h_,(int(can2["height"])-h_)*int(can2["scrollregion"].split(" ")[-1])/int(can2["height"]))

	    return



	if state=="sel_book":


		for i in books3:




			cx,cy=w/2-i[1]+15,i[2]+15
			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:

				sel_book=i[0]
				sel_chapter_()



				return


			cx,cy=w/2+i[1]-15,i[2]+15

			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:


				sel_book=i[0]
				sel_chapter_()


				return


			if w/2-i[1]+15<=e.x<=w/2+i[1]-15:
				if i[2]<=can2.canvasy(e.y)<=i[2]+30:

					sel_book=i[0]
					sel_chapter_()

					return
	elif state=="sel_chapter":

		for i in chapters:


			cx,cy=i[1]+15,i[3]+15
			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:

				sel_chapter=i[0]
				sel_verse_()



				return


			cx,cy=i[1]+i[2]-15,i[3]+15

			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:

				sel_chapter=i[0]
				sel_verse_()


				return


			if i[1]+15<=e.x<=i[1]+i[2]-15:
				if i[3]<=can2.canvasy(e.y)<=i[3]+30:

					sel_chapter=i[0]
					sel_verse_()
					return
	elif state=="sel_verse":

		for i in verses:


			cx,cy=i[1]+15,i[3]+15
			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:

				sel_verse=i[0]
				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
				main()



				return


			cx,cy=i[1]+i[2]-15,i[3]+15

			r=math.sqrt((cx-e.x)**2+(cy-can2.canvasy(e.y))**2)
			if r<=15:

				sel_verse=i[0]
				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
				main()


				return


			if i[1]+15<=e.x<=i[1]+i[2]-15:
				if i[3]<=can2.canvasy(e.y)<=i[3]+30:

					sel_verse=i[0]
					can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
					main()
					return


def can1_b1(e):
	global w,h
	global can1,can2
	global state
	global intro_bts,ar_testament
	global books,books2,book3,book_
	global sel_testament,sel_book,sel_chapter,sel_verse

	if state=="intro":




		for i in intro_bts:


			cx,cy=w/2-i[1]+15,i[2]+15
			r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
			if r<=15:
				if i[0]=="Continue":
					continue_()
				elif i[0]=="Read":
					sel_testament_()

				elif i[0]=="Highlights":
					can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
					view_highlights()


				return


			cx,cy=w/2+i[1]-15,i[2]+15

			r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
			if r<=15:
				if i[0]=="Continue":
					continue_()
				elif i[0]=="Read":
					sel_testament_()

				elif i[0]=="Highlights":
					can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
					view_highlights()

				return


			if w/2-i[1]+15<=e.x<=w/2+i[1]-15:
				if i[2]<=e.y<=i[2]+30:


					if i[0]=="Continue":
						continue_()
					elif i[0]=="Read":
						sel_testament_()

					elif i[0]=="Highlights":
						can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
						view_highlights()
					return

	elif state=="sel_testament":



		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				intro2()
				return

		for i in ar_testament:


			cx,cy=w/2-i[1]+15,i[2]+15
			r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
			if r<=15:

				sel_testament=i[0]
				sel_book_()



				return


			cx,cy=w/2+i[1]-15,i[2]+15

			r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
			if r<=15:


				sel_testament=i[0]
				sel_book_()
				return


			if w/2-i[1]+15<=e.x<=w/2+i[1]-15:
				if i[2]<=e.y<=i[2]+30:




					sel_testament=i[0]
					sel_book_()
					return
	elif state=="sel_book":





		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				sel_testament_()
				return



	elif state=="sel_chapter":

		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				sel_book_()
				return


		s=90

		cx,cy=w/2-s+15,h-50+(50-30)/2+15
		r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
		if r<=15:

			main()



			return


		cx,cy=w/2+s-15,h-50+(50-30)/2+15

		r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
		if r<=15:
			can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
			main()
			return


		if w/2-s+15<=e.x<=w/2+s-15-15:
			if h-50+(50-30)/2<=e.y<=h-50+(50-30)/2+30:

				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
				main()
				return
	elif state=="sel_verse":

		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				sel_chapter_()
				return



		s=90

		cx,cy=w/2-s+15,h-50+(50-30)/2+15
		r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
		if r<=15:

			can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))

			main()



			return


		cx,cy=w/2+s-15,h-50+(50-30)/2+15

		r=math.sqrt((cx-e.x)**2+(cy-e.y)**2)
		if r<=15:
			can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
			main()
			return


		if w/2-s+15<=e.x<=w/2+s-15-15:
			if h-50+(50-30)/2<=e.y<=h-50+(50-30)/2+30:

				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
				main()
				return


	elif state=="main":

		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				if sel_chapter==0:
					sel_chapter_()

				elif sel_chapter!=0:
					sel_verse_()


				return

		xx=int(can2["width"])/3

		if xx-15<=e.x<=xx+15:
			if h-50+(50-30)/2<=e.y<=h-50+(50-30)/2+30:

				if sel_chapter-1>0:
					sel_chapter-=1
				else:
					v=books.index(sel_book)

					if not v==0:

						try:
							sel_book=books[v-1]
							sel_chapter=1
						except:
							pass



				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))

				main()


				return
		if w-xx-15<=e.x<=w-xx+15:
			if h-50+(50-30)/2<=e.y<=h-50+(50-30)/2+30:

				if sel_chapter+1<=len(book[sel_book]):
					sel_chapter+=1
				else:
					v=books.index(sel_book)


					try:
						sel_book=books[v+1]
						sel_chapter=1
					except:
						pass



				can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
				main()

				return

		if 8<=e.x<=42:
			if h-25-10<=e.y<=h-25+10:

				if book_=="NIV":
					book_="KJV"
				elif book_=="KJV":
					book_="NIV"

				main()

				return

	elif state=="view_highlights":

		if w-30-5<=e.x<=w-5:
			if 5<=e.y<=5+30:
				intro2()
				return


		if 8<=e.x<=42:
			if h-25-10<=e.y<=h-25+10:

				if book_=="NIV":
					book_="KJV"
				elif book_=="KJV":
					book_="NIV"

				view_highlights()

				return

def continue_():
	global save_

	global book,book_,sel_testament,sel_book,sel_chapter,sel_verse
	global can2


	try:


		with open("data/save.json", "r") as file:
		    save_ = json.load(file)


		book_,sel_testament,sel_book,sel_chapter,sel_verse,v=save_["save"]



		main()

		can2.yview_moveto(v)
	except:
		pass

ar_testament=[]
def sel_testament_():
	global w,h
	global state
	global can1
	global ar_testament
	global back
	global circle1
	global sel_testament
	global bg2

	sel_testament=0

	state="sel_testament"

	can1.delete("all")
	can2.delete("all")

	can2.place_forget()


	can1.create_image(0,0,image=bg2,anchor="nw")

	can1.create_image(w-30-5,5,image=back,anchor="nw")


	y=(h-(2*30+30))/2
	x=90

	ar=["Old Testament","New Testament"]

	ar_testament=[]

	for i in ar:

		ar_testament.append([i,x,y])

		y+=60

	for i in ar_testament:

		can1.create_image(int(can1["width"])/2-i[1],i[2],image=circle1,anchor="nw")
		can1.create_image(int(can1["width"])/2+i[1]-30,i[2],image=circle1,anchor="nw")

		can1.create_rectangle(int(can1["width"])/2-i[1]+15,i[2], int(can1["width"])/2+i[1]-15,i[2]+30-1,fill="#ff1f83",outline="#ff1f83")

		can1.create_text(w/2,i[2]+15,text=i[0],font=("FreeMono",13),fill="#000000")



books3=[]
bg_=0
def sel_book_():
	global w,h
	global state
	global can1,can2
	global books2,books3
	global back
	global circle1
	global sel_testament
	global sel_book
	global bg2,bg_

	sel_book=0

	state="sel_book"


	if sel_testament=="Old Testament":
		books2=books[:39]

	elif sel_testament=="New Testament":
		books2=books[39:]


	can1.delete("all")
	can2.delete("all")

	can1.create_image(0,0,image=bg2,anchor="nw")

	bg_=can2.create_image(-2.5,-50,image=bg2,anchor="nw")


	#create_polygon(*[0,0, w,0, w,49, 0,49, 0,0], fill="#ff1f83", alpha=0.1,can=can1)

	can1.create_text(w/2,20,text=sel_testament,font=("FreeMono",20),fill="#ffffff")

	can1.create_image(w-30-5,5,image=back,anchor="nw")

	#create_polygon(*[0,h-49, w,h-49, w,h, 0,h, 0,h-49], fill="#ff1f83", alpha=0.1,can=can1)


	y=10

	x=90


	books3=[]

	for i in books2:

		books3.append([i,x,y])


		y+=60


	for i in books3:

		can2.create_image(int(can2["width"])/2-i[1],i[2],image=circle1,anchor="nw")
		can2.create_image(int(can2["width"])/2+i[1]-30,i[2],image=circle1,anchor="nw")

		can2.create_rectangle(int(can2["width"])/2-i[1]+15,i[2], int(can2["width"])/2+i[1]-15,i[2]+30-1,fill="#ff1f83",outline="#ff1f83")


		can2.create_text(int(can2["width"])/2,i[2]+15,text=i[0],font=("FreeMono",13),fill="#000000")

		y=i[2]+30

	y+=10

	can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))

	if y>int(can2["height"]):
		can2["scrollregion"]=(0,0,int(can2["width"]),y)

	can2.place(in_=root,x=2.5,y=50)


	draw_sb()


chapters=[]
def sel_chapter_():
	global w,h
	global can1,can2
	global state
	global sel_book,sel_chapter
	global chapters
	global book
	global bg2,bg_

	sel_chapter=0

	can1.delete("all")
	can2.delete("all")

	state="sel_chapter"


	can1.create_image(0,0,image=bg2,anchor="nw")

	bg_=can2.create_image(-2.5,-50,image=bg2,anchor="nw")



	#create_polygon(*[0,0, w,0, w,49, 0,49, 0,0], fill="#ff1f83", alpha=0.3,can=can1)

	can1.create_text(10,25,text=sel_book,font=("FreeMono",20),fill="#ffffff",anchor="w")
	can1.create_text(w/2,25,text="Select Chapter",font=("FreeMono",20),fill="#ffffff")


	can1.create_image(w-30-5,5,image=back,anchor="nw")



	s=90
	#create_polygon(*[0,h-49, w,h-49, w,h, 0,h, 0,h-49], fill="#ff1f83", alpha=0.3,can=can1)

	can1.create_image(w/2-s,h-50+(50-30)/2,image=circle1,anchor="nw")
	can1.create_image(w/2+s-30,h-50+(50-30)/2,image=circle1,anchor="nw")

	can1.create_rectangle(w/2-s+15,h-50+(50-30)/2,w/2+s-15,h-50+(50-30)/2+30-1,fill="#ff1f83",outline="#ff1f83")

	can1.create_text(w/2,h-50+(50-30)/2+15,text="Read",font=("FreeMono",13),fill="#000000")


	n=1
	n2=0

	if len(book[sel_book])>=4:
		n=len(book[sel_book])/4

		if len(book[sel_book])%4!=0:
			n2=1

	chapters=[]

	sz=50

	c=1
	y=30

	for y_ in range(int(n)+n2):

		xx=(int(can2["width"])-sz*4)/5
		for x in range(4):


			can2.create_image(xx,y,image=circle1,anchor="nw")
			can2.create_image(xx+sz-30,y,image=circle1,anchor="nw")

			can2.create_rectangle(xx+15,y,xx+sz-15,y+30-1,fill="#ff1f83",outline="#ff1f83")



			can2.create_text(xx+sz/2,y+15,text=str(c),font=("FreeMono",13),fill="#000000")

			chapters.append([c,xx,sz,y])

			if c==len(book[sel_book]):
				break			

			c+=1

			xx+=sz+(int(can2["width"])-sz*4)/5


		y+=70


	y==30

	can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
	if y>int(can2["height"]):
		can2["scrollregion"]=(0,0,int(can2["width"]),y)

	can2.place(in_=root,x=2.5,y=50)
	draw_sb()

verses=[]
def sel_verse_():

	global w,h
	global can1,can2
	global state
	global sel_book,sel_chapter,sel_verse
	global verses
	global book
	global bg2,bg_

	sel_verse=0

	can1.delete("all")
	can2.delete("all")

	state="sel_verse"

	can1.create_image(0,0,image=bg2,anchor="nw")

	bg_=can2.create_image(-2.5,-50,image=bg2,anchor="nw")



	can1.create_image(w-30-5,5,image=back,anchor="nw")
	can1.create_text(10,25,text=sel_book+" "+str(sel_chapter) ,font=("FreeMono",20),fill="#ffffff",anchor="w")
	can1.create_text(w/2,25,text="Select Verse" ,font=("FreeMono",20),fill="#ffffff")

	s=90
	can1.create_image(w/2-s,h-50+(50-30)/2,image=circle1,anchor="nw")
	can1.create_image(w/2+s-30,h-50+(50-30)/2,image=circle1,anchor="nw")

	can1.create_rectangle(w/2-s+15,h-50+(50-30)/2,w/2+s-15,h-50+(50-30)/2+30-1,fill="#ff1f83",outline="#ff1f83")

	can1.create_text(w/2,h-50+(50-30)/2+15,text="Read",font=("FreeMono",13),fill="#000000")



	n=1
	n2=0

	if len(book[sel_book][str(sel_chapter)])>=4:

		n=len(book[sel_book][str(sel_chapter)])/4

		if len(book[sel_book][str(sel_chapter)])%4!=0:
			n2=1

	verses=[]

	sz=50

	c=1
	y=30

	for y_ in range(int(n)+n2):

		xx=(int(can2["width"])-sz*4)/5
		for x in range(4):

			


			can2.create_image(xx,y,image=circle1,anchor="nw")
			can2.create_image(xx+sz-30,y,image=circle1,anchor="nw")

			can2.create_rectangle(xx+15,y,xx+sz-15,y+30-1,fill="#ff1f83",outline="#ff1f83")



			can2.create_text(xx+sz/2,y+15,text=str(c),font=("FreeMono",13),fill="#000000")

			verses.append([c,xx,sz,y])

			if c==len(book[sel_book][str(sel_chapter)]):
				break
			c+=1

			xx+=sz+(int(can2["width"])-sz*4)/5


		y+=70


	y+=30

	can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
	if y>int(can2["height"]):
		can2["scrollregion"]=(0,0,int(can2["width"]),y)

	can2.place(in_=root,x=2.5,y=50)
	draw_sb()

intro_bts=[]
def intro2():
	global w,h
	global state
	global can1
	global intro_bts
	global circle1
	global bg2

	state="intro"


	can1.delete("all")
	can2.delete("all")

	can2.place_forget()


	can1.place(in_=root,x=0,y=0)

	can1.create_image(0,0,image=bg2,anchor="nw")

	try:

	    with open("data/save.json", "r") as file:
	        save_ = json.load(file)


	except:
	    save_={}


	ar=[]

	if not save_=={}:
		ar.append("Continue")

	ar.append("Read")
	ar.append("Highlights")


	y=(h-(len(ar)*30+(len(ar)-1)*30))/2

	x=90


	intro_bts=[]

	for i in ar:

		intro_bts.append([i,x,y])


		y+=60


	for i in intro_bts:

		can1.create_image(int(can1["width"])/2-i[1],i[2],image=circle1,anchor="nw")
		can1.create_image(int(can1["width"])/2+i[1]-30,i[2],image=circle1,anchor="nw")

		can1.create_rectangle(int(can1["width"])/2-i[1]+15,i[2], int(can1["width"])/2+i[1]-15,i[2]+30-1,fill="#ff1f83",outline="#ff1f83")

		can1.create_text(w/2,i[2]+15,text=i[0],font=("FreeMono",13),fill="#000000")

t=0
def load():
	global state,t

	if state=="":

		t+=1

		if t>=5:
			intro2()

	root.after(1000,load)

def intro():
	global can1,can2
	global bg

	can1.delete("all")
	can2.delete("all")

	can2.place_forget()


	can1.place(in_=root,x=0,y=0)

	can1.create_image(0,0,image=bg,anchor="nw")


circle1=0
circle2=0
back=0
previous,next_=0,0
bg=0
bg2=0
def load_im():
	global circle1,circle2
	global back
	global previous,next_
	global bg,bg2


	circle1=ImageTk.PhotoImage(file="data/circle1.png")
	circle2=ImageTk.PhotoImage(file="data/circle2.png")
	back=ImageTk.PhotoImage(file="data/back.png")
	previous=ImageTk.PhotoImage(file="data/previous.png")
	next_=ImageTk.PhotoImage(file="data/next.png")
	bg=ImageTk.PhotoImage(file="data/bg.png")
	bg2=ImageTk.PhotoImage(file="data/bg2.png")

state=""
sel_testament=""
sel_book=""
sel_chapter=0
sel_verse=0

book=niv
book_="NIV"

root=tk.Tk()

w,h=1000,600
wd,ht=root.winfo_screenwidth(),root.winfo_screenheight()
root.geometry(str(w)+"x"+str(h)+"+"+str(int((wd-w)/2))+"+"+str(int((ht-h)/2)))
root.resizable(0,0)
root.iconbitmap("data/icon.ico")
root.title("Bible")
can1=tk.Canvas(width=w,height=h,bg="#ffffff",relief="flat",highlightthickness=0,border=0)
can1.bind("<Button-1>",can1_b1)



y1=0

def move_bg():

    global can2
    global y1
    global sb_h
    global bg_
    

    if int(can2.canvasy(0))!=y1:


        y1=int(can2.canvasy(0))

        sb_h=can2.canvasy(0)*int(can2["height"])/int(can2["scrollregion"].split(" ")[-1])
        draw_sb()

        can2.coords(bg_,-2.5,can2.canvasy(-50))

        


def on_release(e):
    global sb_st

    if sb_st==1:
        sb_st=0

def drag(e):

    global can2
    global sb_sz,sb_col,sb_h,sb_st

    if sb_st==1:

        if not e.y<0:


            #can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))

            h=int(can2["height"])/int(can2["scrollregion"].split(" ")[-1])*int(can2["height"])

            if not e.y+h>int(can2["height"]):
                sb_move(e.y,e.y*int(can2["scrollregion"].split(" ")[-1])/int(can2["height"]))
            else:
                sb_move(int(can2["height"])-h-3,(int(can2["height"])-h-3)*int(can2["scrollregion"].split(" ")[-1])/int(can2["height"]))


            move_bg()
            draw_sb()


def update_sb():
    global can2,sb_region,sb_h,psb_h



    if can2["scrollregion"]!=sb_region:

        draw_sb()

        sb_region=can2["scrollregion"]

        move_bg()


    if sb_h!=psb_h:

        draw_sb()

        psb_h=sb_h

        move_bg()







    root.after(1,update_sb)


def draw_sb():
    global can2
    global state
    global sb,sb_sz,sb_region,sb_h,circle2
    global book_,sel_testament,sel_book,sel_chapter,sel_verse

    can2.delete(sb[0])
    can2.delete(sb[1])
    can2.delete(sb[2])

    h=int(can2["height"])/int(can2["scrollregion"].split(" ")[-1])*int(can2["height"])

    sb[0]=can2.create_image(int(can2["width"])-sb_sz-1,can2.canvasy(sb_h),image=circle2,anchor="nw")
    sb[1]=can2.create_rectangle(int(can2["width"])-sb_sz-1,can2.canvasy(sb_h+3),int(can2["width"])-1,can2.canvasy(sb_h+h-3),fill=sb_col,outline=sb_col)
    sb[2]=can2.create_image(int(can2["width"])-sb_sz-1,can2.canvasy(sb_h+h-6),image=circle2,anchor="nw")

    if state=="main":

	    save([book_,sel_testament,sel_book,sel_chapter,sel_verse,can2.canvasy(0)/int(can2["scrollregion"].split(" ")[-1])])


def sb_move(v1,v2):

	global can2
	global sb_h
	global book_,sel_book,sel_chapter,sel_verse
	global yval

	sb_h=v1
	yval=v2/int(can2["scrollregion"].split(" ")[-1])
	can2.yview_moveto(yval)

	#print(can.canvasy(0))

	move_bg()










sb=[0,0,0]
sb_sz=5
sb_col="#ff1f83"
sb_region=()
sb_h=0
psb_h=0
sb_st=0










def on_mousewheel(e):

	global can2,sb_h,bg_

	if int(can2["scrollregion"].split(" ")[-1])>((h-121)-80-10):

		can2.yview_scroll(int(-1*(e.delta/120)), "units")

		sb_h=can2.canvasy(0)*int(can2["height"])/int(can2["scrollregion"].split(" ")[-1])
		draw_sb()
		move_bg()



can2=tk.Canvas(width=w-5,height=h-50*2,bg="#ffffff",relief="flat",highlightthickness=0,border=0)
can2["scrollregion"]=(0,0,int(can2["width"]),int(can2["height"]))
can2.bind("<B1-Motion>",drag)
can2.bind("<Button-1>",can2_b1)
can2.bind("<Button-3>",can2_b3)
can2.bind_all("<MouseWheel>",on_mousewheel)


load_im()
intro()

update_sb()
load()
root.mainloop()

