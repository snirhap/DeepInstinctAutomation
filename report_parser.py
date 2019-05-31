import re
import copy


class ReportParser:
    def __init__(self, report_file_path):
        self.report_file_path = report_file_path
        self.results = {}
        self.current_guard = ''

    def get_most_sleepy_guard(self):
        self.calculate_guards_sleeping_time()
        max_total_sleeptime = 0
        most_sleepy_guard = ''

        for guard in self.results:
            if self.results[guard]['sum_sleep'] > max_total_sleeptime:
                most_sleepy_guard = guard
                max_total_sleeptime = self.results[guard]['sum_sleep']

        if most_sleepy_guard != '':
            most_likely_time = int(self.results[most_sleepy_guard]['sleep_times'].index(max(self.results[most_sleepy_guard]['sleep_times'])))

            if most_likely_time < 10:
                most_likely_time = '00:0{}'.format(most_likely_time)
            else:
                most_likely_time = '00:{}'.format(most_likely_time)

            return 'Guard {} is most likely to be asleep in {}'.format(most_sleepy_guard, most_likely_time)
        else:
            return 'Guards are doing their job'

    def calculate_guards_sleeping_time(self):
        previous_instruction = []

        with open(self.report_file_path, 'r') as report_file:
            for line in report_file.readlines():
                parsed_line = self.parse_line(line)

                if 'begins shift' in parsed_line:
                    if 'falls asleep' not in previous_instruction:  # must be a waking up after falling asleep
                        self.current_guard = parsed_line[2]

                        if self.current_guard not in self.results.keys():  # create meta-data for this guard
                            self.results[self.current_guard] = {}
                            self.results[self.current_guard]['sum_sleep'] = 0
                            self.results[self.current_guard]['sleep_times'] = [0] * 60  # zero list with the size of 60 (for every minute he could be asleep at)
                    else:
                        raise GuardNotAwakeException('Unvalid combination of actions - previous guard must be awake')

                elif 'falls asleep' in parsed_line:
                    if 'falls asleep' in previous_instruction:
                        raise FallAsleepException('Unvalid combination of actions - two falls asleep in a row')

                elif 'wakes up' in parsed_line:
                    if 'falls asleep' in previous_instruction:
                        time_slept = int(parsed_line[1][3:]) - int(previous_instruction[1][3:])
                        self.results[self.current_guard]['sum_sleep'] += time_slept
                        minute_prev = int(previous_instruction[1][3:])
                        minute_cur = int(parsed_line[1][3:])

                        for i in range(minute_prev, minute_cur):
                            self.results[self.current_guard]['sleep_times'][i] += 1
                    else:
                        raise AwakeWithoutAsleepException('Unvalid combination of actions - wakes up must be after falls asleep')

                previous_instruction = copy.deepcopy(parsed_line)


    def parse_line(self, line_to_parse):
        parsed_line = []
        line_to_parse = re.sub('[\[\]]', '', line_to_parse)
        line_to_parse = line_to_parse.split(' ')
        # print(line_to_parse)

        log_date = line_to_parse[0]
        parsed_line.append(log_date)

        log_time = line_to_parse[1]
        parsed_line.append(log_time)

        if 'Guard' in line_to_parse:
            log_guard = line_to_parse[3]
            parsed_line.append(log_guard)

            log_action = (' '.join(line_to_parse[4:])).replace('\n', '')
            parsed_line.append(log_action)
        else:
            current_action = (' '.join(line_to_parse[2:])).replace('\n', '')
            parsed_line.append(current_action)

        return parsed_line

    def print_results(self):
        for guard in self.results:
            print('Guard {}\nTotal sleep time: {}\nSleep List: {}'.format(guard,
                                                                          self.results[guard]['sum_sleep'],
                                                                          self.results[guard]['sleep_times']))
            print('***************\n')


class AwakeWithoutAsleepException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GuardNotAwakeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FallAsleepException(Exception):
    def __init__(self, message):
        super().__init__(message)
