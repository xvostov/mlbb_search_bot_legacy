import asyncio
import random

from db.enums import ROLES
from db.functions import add_profile_to_db

user_ids = [767684418, 1747458435, 5584672860]


"""
user_id=user_id,
nickname=profile_data.get('nickname'),
last_season_rank=profile_data.get('last_season_rank'),
current_rank=profile_data.get('current_rank'),
current_pts=profile_data.get('current_pts', None),
max_rank=profile_data.get('max_rank'),
current_win_rate=profile_data.get('current_win_rate'),
first_role=profile_data.get('first_role'),
second_role=profile_data.get('second_role'),
main_characters=profile_data.get('main_characters'),
voice_communication=True if profile_data.get('voice_communication') == 'да' else False
"""

async def main():
    for i, user in enumerate(user_ids):

        profile = {
            'nickname': f'test-{i+1}',
            'last_season_rank': random.randint(1, 9),
            'current_rank': random.randint(1, 9),
            'current_pts': random.randint(1, 5000+1),
            'max_rank': random.randint(1, 9),
            'current_win_rate': random.randint(30, 65),
            'first_role': random.choice(ROLES.enums),
            'second_role': random.choice(ROLES.enums),
            'main_characters': 'auto_fill',
            'voice_communication': True if random.choice([True, False]) == 'да' else False


        }
        await add_profile_to_db(profile, user)

if __name__ == '__main__':
    asyncio.run(main())