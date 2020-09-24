"""
Log parser
===========

Accepts a filename on the command line.
The file is a Linux-like log file from a system you are debugging.
Mixed in among the various statements are messages indicating
the state of the device. They look like this:

    Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON

The device state message has many possible values, but this program cares
about only three: ``ON``, ``OFF``, and ``ERR``.

Your program will parse the given log file and print out
a report giving how long the device was ``ON``
and the timestamp of any ``ERR`` conditions.
"""

import argparse
import pathlib
import datetime
import typing


def cli_parse() -> pathlib.Path:
    """
    CLI interface to get the logfile path with the ``--log`` argument.

    :return: path of the logfile.
    :rtype: pathlib.Path
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log', required=True, help='Path of the logfile to parse'
    )
    args = parser.parse_args()

    return pathlib.Path(args.log)


def filter_log(
        log: pathlib.Path
) -> typing.List[typing.Tuple[datetime.datetime, str]]:
    """
    Read the logfile and get the timestamp and the status of log
    messages reporting the Device status.

    :param log: file path of the logfile.
    :type log: pathlib.Path
    :return: list of tuples with timestamp and status.
    :rtype: typing.List[typing.Tuple[datetime.datetime, str]]
    """

    filtered_log = []
    with open(log, mode='r', encoding='utf-8') as f:
        for line in f:
            if 'Device State' in line:
                line_elements = line.split()
                # get the status
                status = line_elements[-1]
                # get the time
                timestamp = ' '.join(line_elements[:3])
                timestamp = datetime.datetime.strptime(
                    timestamp, '%b %d %H:%M:%S:%f'
                )

                filtered_log.append((timestamp, status))

    return filtered_log


def compute_uptime(
    filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
) -> float:
    """
    Compute the total uptime in seconds
    between each ``ON`` and ``OFF`` status.

    :param filtered_log: list of tuples with timestamp and status.
    :type filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
    :return: seconds of uptime.
    :rtype: float
    """
    # total seconds passed between as ON status and an OFF status
    uptime_seconds = 0.0

    # I assume the first timestamp has an ON status
    # as it can't be OFF or err if the Device wasn't ON first
    first_timestamp = filtered_log[0][0]

    on_timestamp = first_timestamp
    for timestamp, status in filtered_log:
        # get the timestamp when the Device is ON
        if status == 'ON':
            if timestamp != first_timestamp:
                on_timestamp = timestamp

        # when the Device is OFF, update the total uptime seconds
        elif status == 'OFF':
            off_timestamp = timestamp
            uptime_seconds += (off_timestamp - on_timestamp).total_seconds()

    return uptime_seconds


def check_errors(
    filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
) -> typing.List[str]:
    """
    Get the timestamps associated with the status ``ERR``.

    :param filtered_log: list of tuples with timestamp and status.
    :type filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
    :return: list of timestamps formatted to nice strings.
    :rtype: typing.List[str]
    """

    # list to store timestamps associated with error events
    error_events = [
        timestamp.strftime('%b %d %H:%M:%S:%f')
        for timestamp, status in filtered_log
        if status == 'ERR'
    ]

    return error_events


def prepare_report(
        filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
) -> str:
    """
    Create a string holding the report data.

    :param filtered_log: list of tuples with timestamp and status.
    :type filtered_log: typing.List[typing.Tuple[datetime.datetime, str]]
    :return: report data.
    :rtype: str
    """

    uptime_seconds = compute_uptime(filtered_log)

    error_events = check_errors(filtered_log)

    # create the report
    report = f'⏱ Total uptime seconds: {uptime_seconds:.1f}s'
    report += '\n--------\n\n'
    if not error_events:
        report += '🎉 No error events, hurray 🎉'
    else:
        report += '\n'.join(['⚠ Error events at:', *error_events])

    return report


if __name__ == '__main__':

    log_to_parse = cli_parse()

    log_timestamps = filter_log(log_to_parse)

    log_report = prepare_report(log_timestamps)

    print(log_report)
