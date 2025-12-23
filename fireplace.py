from vpython import *
import random

# Scene setup with cozy dark background
scene = canvas(
    title='Cozy Christmas Fireplace 🔥',
    width=1500,
    height=750,
    background=color.black
)
scene.lights = []
distant_light(direction=vector(0, 1, 0.5), color=color.gray(0.6))  # Soft overhead light

# Fixed logs at the bottom - clearly visible and stationary
log1 = cylinder(pos=vector(-0.4, -0.5, -0.6), axis=vector(0.8, 0, 0), radius=0.15, color=vector(0.4, 0.2, 0.1))
log2 = cylinder(pos=vector(0, -0.45, -0.6), axis=vector(0.7, 0.1, 0), radius=0.13, color=vector(0.35, 0.18, 0.08))
log3 = cylinder(pos=vector(0.4, -0.5, -0.55), axis=vector(0.6, -0.1, 0), radius=0.14, color=vector(0.45, 0.22, 0.1))

# Main flames - start higher so logs are fully visible
flames = []
for i in range(30):
    flame = sphere(
        pos=vector(random.uniform(-0.4, 0.4), random.uniform(-0.2, 0.1), 0),
        radius=random.uniform(0.12, 0.25),
        color=vector(1, random.uniform(0.5, 0.8), random.uniform(0, 0.2)),
        emissive=True,
        opacity=1.0
    )
    flame.velocity = vector(0, random.uniform(0.02, 0.05), 0)
    flame.base_y = -0.2  # Respawn height
    flames.append(flame)

# Sparks - slow, scattered in all directions (including downward)
sparks = []
for i in range(25):
    spark = sphere(
        pos=vector(random.uniform(-0.3, 0.3), random.uniform(-0.3, -0.1), 0),
        radius=random.uniform(0.025, 0.045),
        color=vector(1, random.uniform(0.7, 1), random.uniform(0, 0.3)),
        emissive=True
    )
    spark.velocity = vector(
        random.uniform(-0.025, 0.025),   # Horizontal scatter
        random.uniform(-0.015, 0.04),    # Upward or slightly downward
        random.uniform(-0.015, 0.015)    # Depth scatter
    )
    sparks.append(spark)

# Gentle rising smoke
smoke = []
for i in range(15):
    puff = sphere(
        pos=vector(random.uniform(-0.3, 0.3), random.uniform(-0.1, 0.2), 0),
        radius=random.uniform(0.2, 0.3),
        color=vector(0.3, 0.3, 0.3),
        opacity=0.3
    )
    puff.velocity = vector(0, 0.01, 0)
    smoke.append(puff)

# Main animation loop - 60 FPS for smooth motion
while True:
    rate(60)

    # Animate flames - shrink and fade as they rise
    for flame in flames:
        flame.pos += flame.velocity
        height_ratio = (flame.pos.y + 0.2) / 0.8
        flame.radius = 0.25 * (1 - height_ratio * 0.8)
        flame.opacity = 1 - height_ratio * 0.9

        if flame.pos.y > 0.7 or flame.opacity < 0.1:
            flame.pos = vector(random.uniform(-0.4, 0.4), flame.base_y, 0)
            flame.radius = random.uniform(0.12, 0.25)
            flame.opacity = 1.0
            flame.velocity.y = random.uniform(0.02, 0.05)
            flame.color = vector(1, random.uniform(0.5, 0.8), random.uniform(0, 0.2))

    # Animate sparks - slow motion with gravity
    for spark in sparks:
        spark.pos += spark.velocity
        spark.velocity.y -= 0.001  # Gentle gravity

        if (spark.pos.y > 1.5 or spark.pos.y < -2.5 or
                abs(spark.pos.x) > 2.5 or abs(spark.pos.z) > 0.4):
            spark.pos = vector(random.uniform(-0.3, 0.3), random.uniform(-0.3, -0.1), 0)
            spark.velocity = vector(
                random.uniform(-0.025, 0.025),
                random.uniform(-0.015, 0.04),
                random.uniform(-0.015, 0.015)
            )

    # Animate smoke - slow rise and expansion
    for puff in smoke:
        puff.pos += puff.velocity
        puff.radius += 0.004
        puff.opacity -= 0.002
        if puff.opacity < 0.05:
            puff.pos = vector(random.uniform(-0.3, 0.3), random.uniform(-0.1, 0.2), 0)
            puff.radius = random.uniform(0.2, 0.3)
            puff.opacity = 0.3
