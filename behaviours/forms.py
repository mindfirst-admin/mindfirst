import json

from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from .models import *


def change_aspiration_name(request):
    data = request.POST
    aspiration_name = data['name']
    if aspiration_name == '':
        messages.error(request, 'Please set an aspiration name')
        return HttpResponseRedirect(reverse('behaviours:behaviour_mapping'))

    profile = Profile.objects.get(user=request.user)
    profile.aspiration_name = aspiration_name
    profile.save()

    return JsonResponse('done', safe=False)


def select_behavior(request):
    response_data = request.POST.get('data', None)
    try:
        data = json.loads(response_data)
    except TypeError:
        return HttpResponseRedirect(reverse('main:members_area'))

    if data:
        behaviors = BehaviourMapping.objects.filter(user=request.user).all()
        for i in behaviors:
            i.is_selected = False
            i.save()
        for i in data:
            behavior = BehaviourMapping.objects.filter(user=request.user, id=i).first()
            behavior.is_selected = True
            behavior.save()

    return JsonResponse('done', safe=False)


def delete_behaviour(request):
    response_data = request.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    behavior = BehaviourMapping.objects.filter(user=request.user, id=id_).first()
    behavior.delete()

    messages.success(request, 'Behavior deleted!')
    return JsonResponse('done', safe=False)


def add_behaviour(request):
    response_data = request.POST.get('data', None)
    data = json.loads(response_data)
    data = data[-1]

    title = data['heading']
    description = data['description']
    behaviour_value = '+ve' if data['behavior'] == 1 else '-ve'
    impact = data['impact']
    difficulty = data['feasibility']

    new_behavior = BehaviourMapping(user=request.user, title=title, description=description, value=behaviour_value,
                                    impact=impact, difficulty=difficulty)
    new_behavior.save()

    messages.success(request, 'Behavior added!')
    return JsonResponse('done', safe=False)


def update_behaviour(request):
    response_data = request.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    title = data['heading']
    description = data['description']
    print(data['behavior'])
    behaviour_value = '+ve' if data['behavior'] == 1 else '-ve'
    impact = data['impact']
    difficulty = data['feasibility']

    behavior = BehaviourMapping.objects.filter(user=request.user, id=id_).first()
    behavior.title = title
    behavior.description = description
    behavior.value = behaviour_value
    behavior.impact = impact
    behavior.difficulty = difficulty
    behavior.save()

    messages.success(request, 'Behavior updated!')
    return JsonResponse('done', safe=False)


@csrf_exempt
def get_behaviours(request):
    db_data = BehaviourMapping.objects.filter(user=request.user).all()
    serialized_data = serializers.serialize('json', [i for i in db_data])

    return JsonResponse({'data': json.loads(serialized_data)}, status=200)


def design_positive_habit(request):
    data = request.POST
    id_ = int(data['behaviour_id'])
    after_or_before = data['before_after']
    frequency = data['frequency']
    celebrate = data['celebrate']
    act = data['act_']
    number_of_times = data['number_of_times']
    behaviour = BehaviourMapping.objects.filter(user=request.user, id=id_).first()

    if any(values == '' for key, values in data.items() if key != 'csrfmiddlewaretoken'):
        messages.error(request, 'All input fields need to be appropriately filled')
        return HttpResponseRedirect(reverse('behaviours:habit_design'), behaviour_id=id_)

    try:
        habit_exists = DesignPositiveHabits.objects.get(behaviour=behaviour)
        if habit_exists:
            habit_exists.after_or_before = after_or_before
            habit_exists.frequency = frequency
            habit_exists.act = act
            habit_exists.celebrate = celebrate
            habit_exists.number_of_times = number_of_times
            habit_exists.save()
    except Exception as e:
        new_habit = DesignPositiveHabits(behaviour=behaviour, after_or_before=after_or_before, frequency=frequency,
                                         celebrate=celebrate, act=act, number_of_times=number_of_times)
        new_habit.save()

    messages.success(request, 'Good job designing your habit')
    return HttpResponseRedirect(reverse('main:members_area'))


def design_negative_habits(request):
    data = request.POST
    id_ = int(data['behaviour_id'])
    trigger = data['trigger']
    frequency = data['frequency']
    make_harder = data['make_harder']
    make_less_obvious = data['make_less_obvious']
    number_of_times = data['number_of_times']

    behaviour = BehaviourMapping.objects.filter(user=request.user, id=id_).first()

    if any(values == '' for key, values in data.items() if key != 'csrfmiddlewaretoken'):
        messages.error(request, 'All input fields need to be appropriately filled')
        return HttpResponseRedirect(reverse('main:habit_design'))

    try:
        habit_exists = DesignNegativeHabits.objects.get(behaviour=behaviour)
        if habit_exists:
            habit_exists.trigger = trigger
            habit_exists.frequency = frequency
            habit_exists.make_harder = make_harder
            habit_exists.make_less_obvious = make_less_obvious
            habit_exists.number_of_times = number_of_times
            habit_exists.save()
    except Exception as e:
        new_habit = DesignNegativeHabits(behaviour=behaviour, make_less_obvious=make_less_obvious, frequency=frequency,
                                         trigger=trigger, make_harder=make_harder, number_of_times=number_of_times)
        new_habit.save()

    messages.success(request, 'Good job designing your habit')
    return HttpResponseRedirect(reverse('main:members_area'))


def record_todays_habit(request):
    thumbs_up = request.POST.get('thumbsUp', None)
    thumbs_down = request.POST.get('thumbsDown', None)

    if thumbs_up:
        behaviour = BehaviourMapping.objects.filter(user=request.user, id=thumbs_up).first()

        behaviour.done_today = True
        behaviour.thumbs_up_today += 1
        behaviour.thumbs_up_this_week += 1
        behaviour.save()
    elif thumbs_down:
        behaviour = BehaviourMapping.objects.filter(user=request.user, id=thumbs_down).first()

        behaviour.done_today = False
        behaviour.thumbs_down_today += 1
        behaviour.thumbs_down_this_week += 1
        behaviour.save()

    return JsonResponse('done', safe=False)


def scale_habit(request):
    response_data = request.POST.get('data', None)
    data = json.loads(response_data)

    id_ = data['id']
    behavior = BehaviourMapping.objects.filter(user=request.user, id=id_).first()
    behavior.is_scaled = True
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


def get_weekly_chart_data(request):
    positive_habits_done = json.loads(request.user.profile.all_positive_habits_this_week)
    negative_habits_done = json.loads(request.user.profile.all_scaled_habits_this_week)
    scaled_habit = json.loads(request.user.profile.all_negative_habits_this_week)

    try:
        max_number = max([max(positive_habits_done), max(negative_habits_done), max(scaled_habit)])
    except ValueError:
        max_number = 10

    if max_number < 10:
        max_number = 10

    return JsonResponse(data={
        'positive': positive_habits_done,
        'negative': negative_habits_done,
        'scaled': scaled_habit,
        'max_number': max_number
    })


def get_trimonthly_chart_data(request):
    positive_habits_done = json.loads(request.user.profile.all_positive_habits_in_twelve_weeks)
    negative_habits_done = json.loads(request.user.profile.all_negative_habits_in_twelve_weeks)
    scaled_habit = json.loads(request.user.profile.all_scaled_habits_in_twelve_weeks)

    try:
        max_number = max([max(positive_habits_done), max(negative_habits_done), max(scaled_habit)])
    except ValueError:
        max_number = 10

    if max_number < 10:
        max_number = 10

    return JsonResponse(data={
        'positive': positive_habits_done,
        'negative': negative_habits_done,
        'scaled': scaled_habit,
        'max_number': max_number
    })
