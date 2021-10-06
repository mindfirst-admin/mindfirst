from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers  # to serialize db data
from .models import BehaviourMaps, LimitingBeliefs, BadHabitDesign, GoodHabitDesign
import json
from accounts.models import Profile
from django.contrib import messages


# Create your views here.
@csrf_exempt
def add_new_behaviour(requests):
    response_data = requests.POST.get('data', None)
    data = json.loads(response_data)[-1]

    title = data['heading']
    description = data['description']
    behaviour_value = '+ve' if data['behavior'] == 1 else '-ve'
    impact = data['impact']
    difficulty = data['feasibility']

    new_behavior = BehaviourMaps(user=requests.user, title=title, description=description,
                                 behavior_value=behaviour_value, impact=impact, difficulty=difficulty)
    new_behavior.save()

    messages.success(requests, 'Behavior added!')

    return HttpResponseRedirect(reverse('main:behaviour_mapping'))


@csrf_exempt
def get_behaviors(requests):
    db_data = BehaviourMaps.objects.filter(user=requests.user).all()
    serialized_data = serializers.serialize('json', [i for i in db_data])

    return JsonResponse({'data': json.loads(serialized_data)}, status=200)


@csrf_exempt
def update_behaviour(requests):
    response_data = requests.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    title = data['heading']
    description = data['description']
    behaviour_value = '+ve' if data['behavior'] == 1 else '-ve'
    impact = data['impact']
    difficulty = data['feasibility']

    behavior = BehaviourMaps.objects.filter(user=requests.user, id=id_).first()
    behavior.title = title
    behavior.description = description
    behavior.behavior_value = behaviour_value
    behavior.impact = impact
    behavior.difficulty = difficulty
    behavior.save()

    messages.success(requests, 'Behavior updated!')

    return HttpResponseRedirect(reverse('main:behaviour_mapping'))


@csrf_exempt
def delete_behaviour(requests):
    response_data = requests.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    behavior = BehaviourMaps.objects.filter(user=requests.user, id=id_).first()
    behavior.delete()

    messages.success(requests, 'Behavior deleted!')

    return HttpResponseRedirect(reverse('main:behaviour_mapping'))


def change_aspiration_name(requests):
    data = requests.POST
    aspiration_name = data['name']
    if aspiration_name == '':
        messages.error(requests, 'Please set an aspiration name')
        return HttpResponseRedirect(reverse('main:behaviour_mapping'))

    profile = Profile.objects.get(user=requests.user)
    profile.aspiration_name = aspiration_name
    profile.save()

    return HttpResponseRedirect(reverse('main:behaviour_mapping'))


@csrf_exempt
def go_to_habit_design(requests):
    data = requests.POST
    id_ = data['behaviors']
    if id_:
        requests.session['behavior_id'] = id_

    return HttpResponseRedirect(reverse('main:habit_design'))


def design_good_habit(requests):
    data = requests.POST
    id_ = int(data['behavior_id'])
    after_or_before = data['before_after']
    frequency = data['frequency']
    celebrate = data['celebrate']
    act = data['act_']
    number_of_times = data['number_of_times']
    behavior = BehaviourMaps.objects.filter(user=requests.user, id=id_).first()

    if any(values == '' for key, values in data.items() if key != 'csrfmiddlewaretoken'):
        messages.error(requests, 'All input fields need to be appropriately filled')
        return HttpResponseRedirect(reverse('main:habit_design'))

    try:
        habit_exists = GoodHabitDesign.objects.get(behavior=behavior)
        if habit_exists:
            habit_exists.after_or_before = after_or_before
            habit_exists.frequency = frequency
            habit_exists.act = act
            habit_exists.celebrate = celebrate
            habit_exists.number_of_times = number_of_times
            habit_exists.save()
            print('heet')
    except Exception as e:
        print(e)
        new_habit = GoodHabitDesign(behavior=behavior, after_or_before=after_or_before, frequency=frequency,
                                    celebrate=celebrate, act=act, number_of_times=number_of_times)
        new_habit.save()

    messages.success(requests, 'Good job designing your habit')
    return HttpResponseRedirect(reverse('main:members_area'))  # habit tracker


def design_bad_habit(requests):
    data = requests.POST
    id_ = int(data['behavior_id'])
    trigger = data['trigger']
    frequency = data['frequency']
    make_harder = data['make_harder']
    make_less_obvious = data['make_less_obvious']
    number_of_times = data['number_of_times']

    behavior = BehaviourMaps.objects.filter(user=requests.user, id=id_).first()

    if any(values == '' for key, values in data.items() if key != 'csrfmiddlewaretoken'):
        messages.error(requests, 'All input fields need to be appropriately filled')
        return HttpResponseRedirect(reverse('main:habit_design'))

    try:
        habit_exists = BadHabitDesign.objects.get(behavior=behavior)
        if habit_exists:
            habit_exists.trigger = trigger
            habit_exists.frequency = frequency
            habit_exists.make_harder = make_harder
            habit_exists.make_less_obvious = make_less_obvious
            habit_exists.number_of_times = number_of_times
            habit_exists.save()
    except Exception as e:
        print(e)
        new_habit = BadHabitDesign(behavior=behavior, make_less_obvious=make_less_obvious, frequency=frequency,
                                   trigger=trigger, make_harder=make_harder, number_of_times=number_of_times)
        new_habit.save()

    messages.success(requests, 'Good job designing your habit')
    return HttpResponseRedirect(reverse('main:members_area'))  # habit tracker


@csrf_exempt
def select_behavior(requests):
    response_data = requests.POST.get('data', None)
    data = json.loads(response_data)

    if data:
        behaviors = BehaviourMaps.objects.filter(user=requests.user).all()
        for i in behaviors:
            i.is_selected = False
            i.save()
        for i in data:
            behavior = BehaviourMaps.objects.filter(user=requests.user, id=i).first()
            behavior.is_selected = True
            behavior.save()

    return HttpResponseRedirect(reverse('main:behaviour_mapping'))


@csrf_exempt
def scale_habit(requests):
    response_data = requests.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    behavior = BehaviourMaps.objects.filter(user=requests.user, id=id_).first()
    behavior.is_scaled = True
    behavior.save()

    return HttpResponseRedirect(reverse('main:habit_reporting'))


@csrf_exempt
def record_habit(requests):
    thumbs_up = requests.POST.get('thumbsUp', None)
    thumbs_down = requests.POST.get('thumbsDown', None)

    if thumbs_up:
        behavior = BehaviourMaps.objects.filter(user=requests.user, id=thumbs_up).first()

        behavior.done_today = True
        behavior.thumb_up_clicked += 1
        behavior.thumb_up_week += 1
        behavior.save()
    elif thumbs_down:
        behavior = BehaviourMaps.objects.filter(user=requests.user, id=thumbs_down).first()

        behavior.done_today = False
        behavior.thumb_down_clicked += 1
        behavior.thumb_down_week += 1
        behavior.save()

    return JsonResponse('done', safe=False)


def update_beliefs(request):
    data = request.POST.get('data')

    old_belief = LimitingBeliefs.objects.filter(user=request.user).first()
    if old_belief is not None:
        old_belief.beliefs = data
        old_belief.save()
    else:
        new_belief = LimitingBeliefs(user=request.user, beliefs=data)
        new_belief.save()

    return JsonResponse('done', safe=False)


def get_chart_data(request):
    positive_habits_done = json.loads(request.user.profile.positive_habits_this_week)
    negative_habits_done = json.loads(request.user.profile.negative_habits_this_week)
    scaled_habit = json.loads(request.user.profile.scaled_habits_this_week)

    try:
        max_number = max([max(positive_habits_done), max(negative_habits_done), max(scaled_habit)])
    except ValueError:
        max_number = 10

    if max_number < 10:
        max_number = 10
    else:
        max_number += 2

    return JsonResponse(data={
        'positive': positive_habits_done,
        'negative': negative_habits_done,
        'scaled': scaled_habit,
        'max_number': max_number
    })


def get_weekly_chart_data(request):
    positive_habits_done = json.loads(request.user.profile.positive_habits_in_twelve_weeks)
    negative_habits_done = json.loads(request.user.profile.negative_habits_in_twelve_weeks)
    scaled_habit = json.loads(request.user.profile.scaled_habits_in_twelve_weeks)

    try:
        max_number = max([max(positive_habits_done), max(negative_habits_done), max(scaled_habit)])
    except ValueError:
        max_number = 10

    if max_number < 10:
        max_number = 10
    else:
        max_number += 2

    return JsonResponse(data={
        'positive': positive_habits_done,
        'negative': negative_habits_done,
        'scaled': scaled_habit,
        'max_number': max_number
    })
