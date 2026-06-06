import pandas as pd

rides = [
    "Hey Duggee’s Big Adventure Badge", "The Furchester Hotel", "Big Fun Showtime",
    "CBeebies Land Photo Studio", "Andy’s Adventures Dinosaur Dig", "Battle Galleons",
    "Bluey the Ride: Here Come The Grannies!", "Bugbie-Go-Round", "Congo River Rapids",
    "Cuckoo Cars Driving School", "Gangsta Granny: The Ride", "Get Set Go Tree Top Adventure",
    "Go Jetters Vroomster Zoom Ride", "Haunted Hollow", "Heave Ho",
    "Hex - The Legend of the Towers", "In The Night Garden Magical Boat Ride",
    "JoJo & Gran Gran At Home", "Justin's House Pie-O-Matic Factory",
    "Marauder's Mayhem", "Octonauts Rollercoaster Adventure",
    "Peter Rabbit Hippity Hop", "Raj’s Bouncy Bottom Burp", "Runaway Mine Train",
    "Sharkbait Reef by SEA LIFE", "The Gardens", "The Royal Carousel",
    "Galactica", "Nemesis Reborn", "Nemesis Sub-Terra",
    "Oblivion", "Rita", "Spinball Whizzer", "TH13TEEN",
    "The Smiler", "Toxicator", "Wicker Man"
]

ride_time = {
    "Hey Duggee’s Big Adventure Badge": 3,
    "The Furchester Hotel": 2,
    "Big Fun Showtime": 3,
    "CBeebies Land Photo Studio": 2,
    "Andy’s Adventures Dinosaur Dig": 3,
    "Battle Galleons": 3,
    "Bluey the Ride: Here Come The Grannies!": 3,
    "Bugbie-Go-Round": 2,
    "Congo River Rapids": 4,
    "Cuckoo Cars Driving School": 5,
    "Gangsta Granny: The Ride": 4,
    "Get Set Go Tree Top Adventure": 3,
    "Go Jetters Vroomster Zoom Ride": 3,
    "Haunted Hollow": 3,
    "Heave Ho": 2,
    "Hex - The Legend of the Towers": 5,
    "In The Night Garden Magical Boat Ride": 4,
    "JoJo & Gran Gran At Home": 3,
    "Justin's House Pie-O-Matic Factory": 4,
    "Marauder's Mayhem": 3,
    "Octonauts Rollercoaster Adventure": 3,
    "Peter Rabbit Hippity Hop": 2,
    "Raj’s Bouncy Bottom Burp": 3,
    "Runaway Mine Train": 4,
    "Sharkbait Reef by SEA LIFE": 2,
    "The Gardens": 1,
    "The Royal Carousel": 2,
    "Galactica": 4,
    "Nemesis Reborn": 4,
    "Nemesis Sub-Terra": 3,
    "Oblivion": 3,
    "Rita": 3,
    "Spinball Whizzer": 3,
    "TH13TEEN": 3,
    "The Smiler": 4,
    "Toxicator": 3,
    "Wicker Man": 4
}

# Load CSV matrix
walk_df = pd.read_csv("alton_walk_matrix.csv", index_col=0)

# Clean up spacing issues (important for ride-name matching)
walk_df.index = walk_df.index.str.strip()
walk_df.columns = walk_df.columns.str.strip()

# Convert to dictionary form (same structure you had before)
walk_time = walk_df.to_dict()

# Example usage
print(walk_time["The Smiler"]["Oblivion"])