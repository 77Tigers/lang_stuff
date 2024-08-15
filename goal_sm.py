from dataclasses import dataclass

# money, points, etc.
@dataclass
class Wallet:
    money: int
    assets: list[...]

# text, image, video, etc.
# to be extended
class Component:
    pass

class Text(Component):
    text: str

# not in use rn
class Image(Component):
    url: str

# not in use rn
class Video(Component):
    url: str

class Poll(Component):
    question: str
    options: list[Component]

# post
# a way to both share content and collect data on the user
@dataclass
class Post:
    component: Component

# goal
# a way of measuring a user's progress
# often contains a mini assessment
# it is a question that the user must answer, or a game they must play, etc.
# a special kind of post (or collection of posts)
# RIGHT NOW: just a yes/no question (whole set)
class Goal:
    question_set: list[(Poll, int)] # poll, weight

# User
@dataclass
class User:
    id: int
    name: str
    assets: Wallet
    goal: Goal # goal the user is working towards


# metric
# data collected on the system (user, question, etc.)

# future
# a prediction market on a metric
