

integral = 0
curr_pos = 0


error = targ_pos - curr_pos
integral += error
derivative = error - last_error
pwm = (kp * error) + (ki * integral) + (kd * derivative)

if pwm > 255:
    pwm = 255
elif pwm < -255:
    pwm = -255

last_error = error