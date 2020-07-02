internet = require("internet")

file = io.open("downloaded_data", "w")
for chunk in internet.request("http://localhost:5000/") do
    print(chunk)
    file:write(chunk)
end
file:close()
