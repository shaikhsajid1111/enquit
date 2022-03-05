from django.http import JsonResponse
from users.models import CustomUser, ReportAccount
from django.contrib.auth.models import User
from post.models import Post, ReportOfAnswer, Tags, Vote, Post_Report, Medias, Answer_Vote, Answer, Vault
from django.contrib.auth.decorators import login_required
import cloudinary  # external library
import cloudinary.uploader  # external library

@login_required
def vote_post(request, post_id):
    """view to vote the post's using HTTP request.

    POST http://domain.com/vote_post/<post_id>
    where page_id is integer
    """
    # if it is POST method
    if request.method == "GET":
        user = CustomUser.objects.get(user=request.user)  # fetch the user
        try:
            post = Post.objects.get(post_id=post_id)  # fetch the post
        except Post.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        try:
            # if vote is already done then un-vote by deleting the response
            vote = Vote.objects.get(user=user, post=post)
            vote.delete()  # delete the vote
            return JsonResponse({"status": 200, "message": "Un-voted the post!"})
        except Vote.DoesNotExist:
            # if vote is not done then vote by creating and saving the response
            new_vote = Vote.objects.create(user=user, post=post)
            new_vote.save()
            return JsonResponse({"status": 200, "message": "Voted the post!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def vote_answer(request, answer_id):
    """view to vote the post's answer using HTTP request.

    POST http://domain.com/vote_post/<answer_id>
    where answer_id is integer
    """
    if request.method == "GET":
        user = CustomUser.objects.get(user=request.user)
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        try:
            # if vote is already done then un-vote by deleting the response

            vote = Answer_Vote.objects.get(
                user=user, answer=answer)
            vote.delete()
            return JsonResponse({"status": 200, "message": "Un-voted the answer!"})
        except Answer_Vote.DoesNotExist:
            # if vote is not done then vote by creating and saving the response

            new_vote = Answer_Vote.objects.create(user=user, answer=answer)
            new_vote.save()
            return JsonResponse({"status": 200, "message": "Voted the answer!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def report_post(request, post_id):
    """view to report the post using HTTP request.

    POST http://domain.com/report_post/<post_id>
    where post_id is integer
    """
    if request.method == "GET":

        user = CustomUser.objects.get(user=request.user)
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        new_report, created = Post_Report.objects.get_or_create(
            user=user, post=post)
        if created is True:
            previous_count = post.report_count
            current_count = previous_count + 1
            post.report_count = current_count
            post.save()
        report_counts = post.report_count  # number of reports
        number_of_users = CustomUser.objects.all().count()  # number of total users
        print("Percentage: ", (35/100)*number_of_users)
        # if 35% of total users on the site reports than the post's should be deleted automatically
        if report_counts > (35/100)*number_of_users:
            medias = Medias.objects.filter(post=post)
            for media in medias:
                cloudinary.uploader.destroy(media.public_id)
            post.delete()
        return JsonResponse({"status": 200, "message": "Reported!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def report_answer(request, answer_id):
    """view to report the post using HTTP request.

    POST http://domain.com/report_answer/<answer_id>
    where post_id is integer
    """
    if request.method == "GET":
        user = CustomUser.objects.get(user=request.user)
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        new_report, created = ReportOfAnswer.objects.get_or_create(
            user=user, answer=answer)
        if created is True:
            previous_report_count = answer.report_count
            current_count = previous_report_count + 1
            answer.report_count = current_count
            answer.save()
        report_counts = answer.report_count  # number of reports
        number_of_users = CustomUser.objects.all().count()  # number of total users
        print("Percentage: ", (35/100)*number_of_users)
        # if 2% of total users on the site reports than the post's should be deleted automatically
        if report_counts > (35/100)*number_of_users:
            answer.delete()
        return JsonResponse({"status": 200, "message": "Reported!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def report_account(request, account_id):
    """view to report the post using HTTP request.

    POST http://domain.com/report_account/<account_id>
    where account_id is integer
    """
    if request.method == "GET":
        user = CustomUser.objects.get(user=request.user)
        try:
            user_report = User.objects.get(id=account_id)
            account_to_report = CustomUser.objects.get(user=user_report)
        except CustomUser.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        new_report, created = ReportAccount.objects.get_or_create(
            user=user, report=account_to_report)
        if created is True:
            previous_count = account_to_report.report_count
            current_count = previous_count + 1
            account_to_report.report_count = current_count
            account_to_report.save()
        report_counts = account_to_report.report_count  # number of reports
        number_of_users = CustomUser.objects.all().count()  # number of total users
        print("Percentage: ", (35/100)*number_of_users)
        # if 15% of total users on the site reports than the post's should be deleted automatically
        if report_counts > ((35/100)*number_of_users):
            account_to_report.delete()
            account_to_report.user.delete()
            print("Deleted the account!")
        return JsonResponse({"status": 200, "message": "Reported!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def delete_answer(request, answer_id):
    """view to get the user's posts using HTTP request.
    GET http://domain.com/delete_answer/<answer_id>
    answer_id is integer
    """
    if request.method == "GET":
        user = request.user  # fetch the user
        custom_user = CustomUser.objects.get(
            user=user)  # fetch the custom user
        try:
            # find the answer by its id
            answer = Answer.objects.get(id=answer_id)
        except:
            answer = None  # if answer is not found than set it to None
        # if the answer is not None and the user is the answer owner
        if answer is not None and answer.user == custom_user:
            answer.delete()
            return JsonResponse({"status": 200, "message": "Deleted Successfully!"})
        else:
            return JsonResponse({"status": 403, "message": "Invalid Access!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


@login_required
def save_answer(request, post_id):
    """view to save the post's using HTTP request.

    POST http://domain.com/save_answer/<post_id>
    where post_id is integer
    """
    if request.method == "GET":
        user = CustomUser.objects.get(user=request.user)
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Does not exists!"})
        try:
            item = Vault.objects.get(user=user, post=post)
            item.delete()
            return JsonResponse({"status": 200, "message": "Unsaved the answer!"})
        except Vault.DoesNotExist:
            item = Vault.objects.create(user=user, post=post)
            item.save()
            return JsonResponse({"status": 200, "message": "Saved the answer!"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})




@login_required
def fetch_answer_replies(request,parent_id,page_number):
  if request.method == "GET":
    try:
      offset = (int(page_number)*10)-10  # number of entry to leave
      limits = int(page_number)*10  # number of entry limit
      parent = Answer.objects.get(id=parent_id)
      replies = Answer.objects.filter(parent=parent)[offset:limits]
      replies_list = []
      custom_user = CustomUser.objects.get(user=request.user)
      for reply in replies:
        try:
          # count number of votes
          votes = Answer_Vote.objects.filter(answer=reply).count()
        except Vote.DoesNotExist:
          # if no vote exists, set the number to 0
          votes = 0
        already_voted = Answer_Vote.objects.filter(
                    user=custom_user, answer=reply) and True or False
        temp_data = {}
        temp_data['reply'] = {
          "text": reply.text,
          "posted_on": reply.timestamp,
          "already_voted" : already_voted,
          "votes" : votes
        }
        temp_data['author'] = {
          "user_id": reply.user.id,
          "username" : reply.user.user.username,
          "profile_media": reply.user.profile_picture_link,
          "is_verified": reply.user.is_verified
        }
        replies_list.append(temp_data)
      return JsonResponse({"status":200,"message":"success","data":replies_list})
    except Exception as ex:
      print(ex)
      return JsonResponse({"status":400,"message":str(ex)})
  else:
    return JsonResponse({"status": 405, "message": "Method Not Allowed"})



@login_required
def fetch_answers(request, post_id, page_number):
    """
    view to get the answers using HTTP request.

    GET http://domain.com/fetch_post_answers/<post_id>/<page_number>
    post_id is integer
    page_number is integer
    """
    if request.method == "GET":
        try:
            offset = (int(page_number)*10)-10  # number of entry to leave
            limits = int(page_number)*10  # number of entry limit
            try:
                custom_user = CustomUser.objects.get(
                    user=request.user)  # get the user
            except CustomUser.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Does not exists!", "posts_data": []})
            # get the posts within limit and offset range
            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"status": 403, "answers": []})
            answers = Answer.objects.filter(
                post=post, parent=None)[offset:limits]
            posts_data = []  # list to hold the data
            for answer in answers:
                data = {}  # for holding post's data temporarily
                already_voted = Answer_Vote.objects.filter(
                    user=custom_user, answer=answer) and True or False
                try:
                    # count number of votes
                    votes = Answer_Vote.objects.filter(answer=answer).count()
                except Vote.DoesNotExist:
                    # if no vote exists, set the number to 0
                    votes = 0
                data['votes'] = votes  # enter the data into dictionary
                replies_list = []
                try:
                    replies = Answer.objects.filter(parent=answer)
                except:
                    replies = []
                for reply in replies:
                    replies_list.append({
                        "answer_id": reply.id,
                        "text": reply.text,
                        "posted_on": reply.timestamp
                    })
                answer_data_temp = {
                    # parse the post's data
                    "answer_id": answer.id,
                    "text": answer.text,
                    "posted_on": answer.timestamp,
                }
                author_temp_data = {
                    "user_id": answer.user.id,
                    "username": answer.user.user.username,
                    "profile_media": answer.user.profile_picture_link,
                    "is_verified": answer.user.is_verified
                }
                try:
                    tags = Tags.objects.filter(tag=post)
                    tags = [tag.text for tag in tags]
                except Tags.DoesNotExist:
                    tags = []
                # assign the data with respective keys
                data['author'] = author_temp_data
                data['answer'] = answer_data_temp
                data['answer']['replies'] = replies_list
                data['already_voted'] = already_voted
                data['tags'] = tags
                data['username'] = post.username()
                data['profile_picture_link'] = post.author.profile_picture_link
                posts_data.append(data)
                # print(posts_data)
                # send the data to home page as well
            return JsonResponse({"status": 200, "answers": posts_data})
        except Exception as ex:
            print(ex)
            return JsonResponse({"status": 400, "answers": []})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


