from allauth.socialaccount.models import SocialAccount


def discord_info(request):
    if request.user.is_authenticated:
        try:
            base = "https://cdn.discordapp.com/avatars/"
            social_account = SocialAccount.objects.get(user=request.user, provider="discord")
            user_id = social_account.extra_data["id"]
            avatar = social_account.extra_data["avatar"]
            extension = ".png"
            if avatar.startswith("a_"):
                extension = ".gif"
            return {
                "avatar_url": f"{base}{user_id}/{avatar}{extension}",
                "discord_username": social_account.extra_data["username"],
                "discriminator": social_account.extra_data["discriminator"],
                "id": user_id,
            }
        except:
            return {
                "avatar_url": "https://discordapp.com/assets/dd4dbc0016779df1378e7812eabaa04d.png",
                "discord_username": "Anonymous",
            }
    else:
        return {}
