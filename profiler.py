from models import load_interests, save_interest

class Profiler:

    def __init__(self, user_id, persona):

        self.user_id = user_id
        self.persona = persona
        self.global_interests = load_interests(user_id)

    def update_interest(self, topic):

        topic = topic.lower()

        new_weight = self.global_interests.get(topic, 0.5) + 0.3

        self.global_interests[topic] = new_weight

        save_interest(self.user_id, topic, new_weight)

    def get_top_interests(self):

        sorted_interests = sorted(
            self.global_interests.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [i[0] for i in sorted_interests[:5]]