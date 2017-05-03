








class Sentient_CNC:

    def __init__(self):
        self.presented_by = 'Josh Zastrow'

















    def Current_Situation():













        print('In today\'s manufacturing environment...')

        variables = dict({
            'Technology': 'Powerful and quickly accelerating.. data hungry',
            'DataSource': 'Uncollected but valuable data from Machines',
            'Machinists': 'Very talented, but few in number',
            'CNCmachine': 'Actually many, more machines than skilled machinists',
            'AnEngineer': 'Dedicated to change the world, knowledgable, driven'})

        return variables












    def Complications():
        '''
        I asked our lead machinist, George, the amount of time
        he could leave his machine running unattended.
        His answer was 'zero'.
        '''








        print('Can we solve our problems with A.I?')

        # Internal
        costly_downtime = set(['LIMITED LABOR',
                               'FREQUENT SETUP',
                               'TOOL BREAKAGE',
                               'PROGRAMMING TIME',
                               'CHIPS WRAPPING'])

        # External
        curr_technology = set(['Industrial IoT',
                               'Machine Learning',
                               'Big Data',
                               'Cloud Computing'])

        return costly_downtime | curr_technology












    def The_Question():












        # Think Big:
        Question1 = "How Can We Convert Down Time " + \
                    "to Money Making Up Time?\n"
        # Think Big:
        Question2 = "How Can We Extend " + \
                    "Our Current Labor Abilities and Capabilites?\n"
        # Think Big:
        Question3 = "How Can We Avoid " + \
                    "Catostrophic Failures On Our Machines?\n"
        # Think Big:
        Question4 = "How Can We Lower " + \
                    "The Skills Gap For New CNC Machinists?\n"
        # Think Big:
        Question5 = "How Can We Bring " + \
                    "Aritifial Intelligence to Manufacturing?\n"

        return Question1 + Question2 + Question3 + Question4 + Question5













    def The_Solution():














        print('We can build an IoT device that will supervise the machine.')

        super_machinist = 'skilled machinist' + 'intelligent assistant'

        # Metrics for success
        solution = {'MoreUptime': '30 minutes more up time per machine per day',
                    'Detection': 'Tool breakage detection - 100% Accurate',
                    'Generalized' : 'Adaptable to any CNC Machine',
                    'PlugAndPlay': 'No Behavior change needed to use device',
                    'Production': '10 percent mprovement in daily output'}

        return solution













pitch_deck = Sentient_CNC
situation = pitch_deck.Current_Situation()
with open("Pitch Deck.txt", "w") as text_file:
    print('Auto Generated Meeting notes:\n', file=text_file)
    [print(key_point, ':', situation[key_point], file=text_file) \
    for key_point in situation]
    print(file=text_file)
    print('\n'.join(pitch_deck.Complications()), end='\n\n', file=text_file)
    print(pitch_deck.The_Question(), file=text_file)
    solution = pitch_deck.The_Solution()
    [print('{}\t-\t{}'.format(k, solution[k]), file=text_file) for k in solution]
