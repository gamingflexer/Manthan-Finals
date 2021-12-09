import twint

#ky=["ISIS","Khalistan","WadhawaSinghBabbar","khalistan","Airportbombing","Khalistanmovement","Inter-ServicesIntelligence","Khalistanisympathisers"]


c = twint.Config()

#for k in ky:

c.Search = "ISIS"
c.Limit= 100
c.Min_likes = 3
c.Custom["tweet"] = ["username","tweet","replies_count","retweets_count",]
c.Output="10.csv"
#c.Store_json=True

c.Hide_output = True

twint.run.Search(c)








