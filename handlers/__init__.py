from loader import dp

from .base import *
from .profile import *
from .matching import *
from .filter import *
from .feedback import *
from .admins import *

from .states import *
from callback_filters import like_dislike_callback_filter



# Profile
dp.register_message_handler(new_profile_cmd_handler, commands=['new_profile'])
dp.register_message_handler(new_profile_nickname_handler, state=NewProfile.nickname)
dp.register_callback_query_handler(last_season_rank_callback_handler, lambda callback_query: True,
                                   state=NewProfile.last_season_rank)
dp.register_callback_query_handler(current_rank_callback_handler, lambda callback_query: True,
                                   state=NewProfile.current_rank)
dp.register_message_handler(new_profile_current_pts_handler, state=NewProfile.current_pts)
dp.register_callback_query_handler(new_profile_max_rank_callback_handler, lambda callback_query: True,
                                   state=NewProfile.max_rank)
dp.register_message_handler(new_profile_current_win_rate_handler, state=NewProfile.current_win_rate)
dp.register_callback_query_handler(new_profile_first_role_callback_handler, lambda callback_query: True,
                                   state=NewProfile.first_role)
dp.register_callback_query_handler(new_profile_second_role_callback_handler, lambda callback_query: True,
                                   state=NewProfile.second_role)
dp.register_message_handler(new_profile_main_characters, state=NewProfile.main_characters)
dp.register_callback_query_handler(new_profile_voice_communication_callback_handler, lambda callback_query: True,
                                   state=NewProfile.voice_communication)
dp.register_callback_query_handler(new_profile_final_callback_handler, lambda callback_query: True,
                                   state=NewProfile.final)
dp.register_message_handler(delete_profile_cmd_handler, commands=['delete_profile'])
dp.register_callback_query_handler(delete_profile_callback_handler, lambda callback_query: True,
                                   state=DeleteProfile.confirmation)
dp.register_message_handler(check_profile_handler, commands=['check_profile'])

# Matching
dp.register_callback_query_handler(like_dislike_callback_handler, like_dislike_callback_filter)

# User Filter
dp.register_message_handler(new_filter_cmd_handler, commands=['new_filter'])
dp.register_callback_query_handler(new_filter_min_rank, lambda callback_query: True,
                                   state=NewFilter.min_rank)
dp.register_message_handler(new_filter_min_pts_handler, state=NewFilter.min_pts)
dp.register_message_handler(new_filter_min_win_rate_handler, state=NewFilter.min_win_rate)
dp.register_callback_query_handler(new_filter_voice_communication_callback_handler, lambda callback_query: True,
                                   state=NewFilter.voice_communication)
dp.register_callback_query_handler(new_filter_final_callback_handler, lambda callback_query: True,
                                   state=NewFilter.final)
dp.register_message_handler(delete_filter_cmd_handler, commands=['delete_filter'])
dp.register_callback_query_handler(delete_filter_callback_handler, lambda callback_query: True,
                                   state=DeleteFilter.confirmation)
dp.register_message_handler(check_filter, commands=['check_filter'])
# Base
dp.register_message_handler(start_cmd_handler, commands=['start', 'help'])
dp.register_message_handler(rules_cmd_handler, commands=['rules'])
dp.register_callback_query_handler(callback_handler_without_context, lambda callback_query: True)

# Feedback
dp.register_message_handler(feedback_cmd_handler, commands=['feedback'])
dp.register_message_handler(feedback_handler, state=FeedBack.user_fb)

# Admins
dp.register_message_handler(say_all_cmd_handler, commands=['say_all'])
dp.register_message_handler(notification_handler, state=AdminNotification.notification)