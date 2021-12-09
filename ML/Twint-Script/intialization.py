import twint

#ky=["ISIS","Khalistan","WadhawaSinghBabbar","khalistan","Airportbombing","Khalistanmovement","Inter-ServicesIntelligence","Khalistanisympathisers"]


c = twint.Config()

#for k in ky:
c.Search = "ISIS"
c.Limit= 300
c.Min_likes = 3
c.Custom["tweet"] = ["id", "username","tweet"]
c.Output="10.json"
c.Store_json=True

c.Hide_output = True

twint.run.Search(c)








