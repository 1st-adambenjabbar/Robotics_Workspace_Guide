# 🏗️ Object-Oriented Programming — Complete Guide
> **C · C++ · Python · Java**
> Every concept, keyword, and mechanism explained from scratch 🐚

---

# 📑 Table of Contents

1. [What is OOP and Why it Exists](#1-what-is-oop-and-why-it-exists)
2. [How Class Files Are Organised](#2-how-class-files-are-organised)
3. [The 4 Pillars of OOP](#3-the-4-pillars-of-oop)
4. [Classes & Objects](#4-classes--objects)
5. [Attributes — Data Inside a Class](#5-attributes--data-inside-a-class)
6. [Methods — Behaviour Inside a Class](#6-methods--behaviour-inside-a-class)
7. [Constructors & Destructors](#7-constructors--destructors)
8. [Access Modifiers — public · private · protected](#8-access-modifiers--public--private--protected)
9. [Inheritance — Building on Existing Classes](#9-inheritance--building-on-existing-classes)
10. [Polymorphism — One Interface Many Behaviours](#10-polymorphism--one-interface-many-behaviours)
11. [Abstract Classes & Interfaces](#11-abstract-classes--interfaces)
12. [Static Members](#12-static-members)
13. [Special Methods & Operator Overloading](#13-special-methods--operator-overloading)
14. [Templates & Generics](#14-templates--generics)
15. [Memory Management](#15-memory-management)
16. [OOP in C — Simulating with Structs](#16-oop-in-c--simulating-with-structs)
17. [Design Patterns](#17-design-patterns)
18. [Full Robot Class Example — All 4 Languages](#18-full-robot-class-example--all-4-languages)
19. [Language Comparison Cheat Sheet](#19-language-comparison-cheat-sheet)

---

# 1. What is OOP and Why it Exists

## The problem OOP solves

Imagine writing a robot program **without** OOP — just functions and variables:

```c
// Without OOP — messy, unorganised
float robot1_x = 0.0, robot1_y = 0.0, robot1_speed = 0.5;
float robot2_x = 0.0, robot2_y = 0.0, robot2_speed = 0.3;

void move_robot1() { robot1_x += robot1_speed; }
void move_robot2() { robot2_x += robot2_speed; }
void stop_robot1() { robot1_speed = 0; }
void stop_robot2() { robot2_speed = 0; }
// What if you have 10 robots? 100?
```

With OOP — organised, scalable:

```python
# With OOP — clean, reusable
class Robot:
    def __init__(self, speed):
        self.x = 0.0
        self.speed = speed

    def move(self):
        self.x += self.speed

    def stop(self):
        self.speed = 0.0

robot1 = Robot(speed=0.5)
robot2 = Robot(speed=0.3)
robots = [Robot(speed=i * 0.1) for i in range(100)]   # 100 robots, 1 line
```

## The core idea

**OOP** = **O**bject-**O**riented **P**rogramming.

The idea: model your program as a collection of **objects** that interact with each other — just like the real world.

```
Real world:                OOP equivalent:
────────────────────────────────────────────
A car                  →   Car class
  has a colour         →     .colour attribute
  has a speed          →     .speed attribute
  can accelerate       →     .accelerate() method
  can brake            →     .brake() method

Your car               →   Car instance (object)
My car                 →   Another Car instance
```

> - **class** — the **blueprint** (the design). Like an architectural plan for a house.
> - **object** (or **instance**) — a **concrete thing** built from the blueprint. Like an actual house built from the plan.
> - **attribute** (or **field** / **member variable**) — **data** stored in an object (the house's colour, size).
> - **method** (or **member function**) — **behaviour** of an object (the house's alarm system, door opening).

---

# 2. How Class Files Are Organised

This is one of the first things that confuses beginners: **where do you actually put your classes?** The answer depends on the language.

---

## 🐍 Python — One or many classes per `.py` file

Python is the most flexible. There is **no enforced rule** — you put classes wherever makes sense.

```
my_project/
├── main.py              ← entry point (runs the program)
├── robot.py             ← Robot class
├── motor.py             ← Motor class
└── utils/
    ├── __init__.py      ← marks this folder as a Python package
    └── math_helpers.py  ← utility functions/classes
```

**`robot.py`** — defines the class:
```python
# robot.py
class Robot:
    def __init__(self, name, speed):
        self.name  = name
        self.speed = speed

    def move(self):
        self.x += self.speed
```

**`main.py`** — imports and uses it:
```python
# main.py
from robot import Robot        # import Robot from robot.py
from motor import Motor        # import Motor from motor.py

robot = Robot("R2D2", 0.5)
robot.move()
```

**Convention (not enforced):**
- One class per file when the class is large
- Multiple small related classes can share a file
- File name = lowercase snake_case: `robot.py`, `ground_robot.py`
- Class name = PascalCase: `Robot`, `GroundRobot`

> - `import` — tells Python to load another file and make its contents available.
> - `from robot import Robot` — import **only** the `Robot` class from `robot.py`, not everything in the file.
> - `import robot` — imports the whole module; then access with `robot.Robot(...)`.
> - `__init__.py` — an empty (or not) file that tells Python "this folder is a package". Allows imports like `from utils.math_helpers import clamp`.
> - **module** — any `.py` file. Python's basic unit of code organisation.
> - **package** — a folder containing an `__init__.py`. Groups related modules.

---

## ⚙️ C++ — Header + Source file split (`.h` / `.cpp`)

C++ splits every class across **two files**:

| File | Extension | Contains |
|------|-----------|---------|
| **Header file** | `.h` or `.hpp` | Class declaration (structure, method signatures) |
| **Source file** | `.cpp` | Method implementations (actual code) |

```
my_project/
├── main.cpp             ← entry point (contains main())
├── Robot.h              ← Robot class declaration
├── Robot.cpp            ← Robot method implementations
├── Motor.h
├── Motor.cpp
└── CMakeLists.txt       ← build system (tells compiler what to compile)
```

**`Robot.h`** — declares the class (the contract):
```cpp
// Robot.h
#pragma once
// #pragma once = include guard: prevents this header from being
// included more than once in the same compilation unit.
// Alternative: #ifndef ROBOT_H / #define ROBOT_H / #endif

#include <string>   // include standard library headers needed here

class Robot {
public:
    Robot(std::string name, double speed);   // constructor DECLARATION
    ~Robot();                                // destructor DECLARATION

    void   move(double distance);            // method DECLARATION
    void   stop();
    double getX() const;
    std::string getName() const;

private:
    std::string name_;    // member variables DECLARED here
    double      speed_;
    double      x_;
};
// ← NO implementation here — just declarations
```

**`Robot.cpp`** — implements the class:
```cpp
// Robot.cpp
#include "Robot.h"       // include OUR header (quotes = local file)
#include <iostream>      // include standard library (angle brackets = system)

// Constructor implementation
// Robot:: = scope resolution — "this belongs to the Robot class"
Robot::Robot(std::string name, double speed)
    : name_(name), speed_(speed), x_(0.0)    // member initializer list
{
    std::cout << "Robot " << name_ << " created.\n";
}

Robot::~Robot() {
    std::cout << "Robot " << name_ << " destroyed.\n";
}

void Robot::move(double distance) {
    x_ += distance;
}

void Robot::stop() {
    speed_ = 0.0;
}

double Robot::getX() const {
    return x_;
}

std::string Robot::getName() const {
    return name_;
}
```

**`main.cpp`** — uses the class:
```cpp
// main.cpp
#include "Robot.h"       // include the header to know the class interface
#include <iostream>

int main() {
    Robot r1("R2D2", 0.5);    // compiler knows this from Robot.h
    r1.move(1.0);
    std::cout << r1.getX() << "\n";

    Robot* r2 = new Robot("C-3PO", 0.3);
    r2->move(2.0);
    delete r2;

    return 0;
}
```

**Why split into `.h` and `.cpp`?**
```
Without split:
  main.cpp includes robot_full.cpp → includes motor_full.cpp → ...
  Every file recompiles everything → SLOW, messy

With split:
  main.cpp   → only includes Robot.h   (fast: just declarations)
  Robot.cpp  → compiled separately once
  Linker     → connects main.o + Robot.o + Motor.o = executable
```

> - `#pragma once` — a **preprocessor directive**: tells the compiler to only process this file once, even if `#include "Robot.h"` appears in many `.cpp` files. Prevents duplicate class definitions.
> - `#include "file.h"` — local file (your project). Uses **quotes**.
> - `#include <file>` — system/library header. Uses **angle brackets**.
> - `Robot::` — **scope resolution operator**. Outside the class body, `Robot::move` means "the `move` function that belongs to `Robot`".
> - **declaration** — tells the compiler that something *exists* and what its signature is. No code.
> - **definition** — provides the actual code / memory.
> - **linker** — after compilation, joins all `.o` object files into one executable. It matches declarations to definitions.
> - `CMakeLists.txt` — the build configuration file for **CMake** (most common C++ build system). Tells it which `.cpp` files to compile and how to link them.

**Typical CMakeLists.txt for a small project:**
```cmake
cmake_minimum_required(VERSION 3.15)
project(MyRobot)
set(CMAKE_CXX_STANDARD 17)

add_executable(my_robot
    main.cpp
    Robot.cpp
    Motor.cpp
)
```

**Alternative — Header-only (`.hpp`):**
```cpp
// Robot.hpp — declaration AND implementation in one file
// Used for templates (must be in header) and small utility classes
#pragma once

class Robot {
public:
    Robot(std::string name) : name_(name) {}   // inline implementation
    void move() { x_ += speed_; }              // inline implementation
private:
    std::string name_;
    double speed_ = 0.5, x_ = 0.0;
};
```

> - **inline** — when implementation is inside the class body in the header. The compiler can optimise these (no function call overhead). Required for **template classes** (templates must be fully visible at compile time).
> - `.hpp` — alternative extension for C++ headers. Signals "this is C++, not C". Both `.h` and `.hpp` work — team convention decides.

---

## ☕ Java — One public class per `.java` file (enforced)

Java **enforces** a strict rule: **one `public` class per file, and the filename must match the class name exactly.**

```
my_project/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── myrobot/           ← package folder structure
│   │               ├── Main.java      ← contains class Main (entry point)
│   │               ├── Robot.java     ← contains class Robot
│   │               ├── GroundRobot.java
│   │               ├── DroneRobot.java
│   │               └── Motor.java
│   └── test/
│       └── java/
│           └── com/myrobot/
│               └── RobotTest.java     ← unit tests
└── pom.xml                            ← Maven build config (or build.gradle for Gradle)
```

**`Robot.java`**:
```java
// Robot.java
package com.myrobot;          // declares which package this class belongs to
// Package = folder path with dots instead of slashes
// com/myrobot/ → com.myrobot

import java.util.ArrayList;   // import other classes you need
import java.util.List;

public class Robot {           // public class name MUST match filename "Robot.java"
    protected String name;
    protected double speed;
    protected double x = 0.0;

    public Robot(String name, double speed) {
        this.name  = name;
        this.speed = speed;
    }

    public void move(double distance) {
        x += distance;
    }

    @Override
    public String toString() {
        return "Robot(" + name + ") at x=" + x;
    }
}
```

**`GroundRobot.java`**:
```java
// GroundRobot.java
package com.myrobot;

public class GroundRobot extends Robot {    // one class, one file
    private double wheelRadius;

    public GroundRobot(String name, double speed, double wheelRadius) {
        super(name, speed);
        this.wheelRadius = wheelRadius;
    }

    @Override
    public String toString() {
        return "GroundRobot(" + name + ")";
    }
}
```

**`Main.java`**:
```java
// Main.java
package com.myrobot;

// Same package → no import needed
// Different package → import com.otherpackage.OtherClass;

public class Main {
    public static void main(String[] args) {    // entry point
        Robot r = new GroundRobot("Rover", 0.5, 0.05);
        r.move(1.0);
        System.out.println(r);
    }
}
```

> - `package com.myrobot` — declares the namespace. The folder structure **must match** the package name: `com/myrobot/Robot.java` → `package com.myrobot`.
> - **Why reverse domain names?** (`com.myrobot`) — convention to guarantee uniqueness globally. `com.google.utils` won't clash with `com.apple.utils`.
> - `import` — brings another class into scope. Classes in the **same package** don't need imports.
> - `public static void main(String[] args)` — the **program entry point**. Exactly one class per project has this method. Java starts execution here.
> - `pom.xml` — **Maven** build config. Lists dependencies, compilation settings, plugins.
> - `build.gradle` — **Gradle** alternative to Maven. More modern, scripted in Groovy or Kotlin.

**Java: Can you have multiple classes in one file?**
```java
// Robot.java
public class Robot { ... }          // ✅ public — must match filename

class HelperClass { ... }           // ✅ package-private — allowed in same file
// BUT: only ONE public class per file
// class AnotherPublicClass { ... } // ❌ would be a compiler error
```

---

## 🔵 C — Multiple structs per `.c` / `.h` file

C has no classes, but the same header/source split applies.

```
my_project/
├── main.c
├── robot.h          ← struct declaration + function signatures
├── robot.c          ← function implementations
├── motor.h
└── motor.c
```

**`robot.h`**:
```c
// robot.h
#ifndef ROBOT_H      // include guard (older C style, still common)
#define ROBOT_H

typedef struct {
    char   name[50];
    double speed;
    double x;
} Robot;

// Function declarations (signatures only)
Robot* Robot_new(const char* name, double speed);
void   Robot_delete(Robot* r);
void   Robot_move(Robot* r, double distance);
double Robot_getX(const Robot* r);

#endif  // ROBOT_H
```

**`robot.c`**:
```c
// robot.c
#include "robot.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

Robot* Robot_new(const char* name, double speed) {
    Robot* r = (Robot*)malloc(sizeof(Robot));
    if (!r) return NULL;
    strncpy(r->name, name, 49);
    r->name[49] = '\0';
    r->speed = speed;
    r->x     = 0.0;
    return r;
}

void Robot_delete(Robot* r) {
    free(r);
}

void Robot_move(Robot* r, double distance) {
    r->x += distance;
}

double Robot_getX(const Robot* r) {
    return r->x;
}
```

**`main.c`**:
```c
// main.c
#include "robot.h"
#include <stdio.h>

int main(void) {
    Robot* r = Robot_new("R2D2", 0.5);
    Robot_move(r, 1.5);
    printf("x = %.2f\n", Robot_getX(r));
    Robot_delete(r);
    return 0;
}
```

> - `#ifndef ROBOT_H` / `#define ROBOT_H` / `#endif` — the classic **include guard** pattern. Alternative to `#pragma once`. Works in both C and C++.
> - **Naming convention in C** — since there are no namespaces, prefix function names with the "class" name: `Robot_new`, `Robot_move`. Avoids naming collisions.

---

## 📁 Summary — File naming at a glance

| Language | File(s) per class | Extensions | Naming convention |
|----------|------------------|------------|-------------------|
| **Python** | 1 `.py` (flexible) | `.py` | `robot.py` → `class Robot` |
| **C++** | 2 files (header + source) | `.h`/`.hpp` + `.cpp` | `Robot.h` + `Robot.cpp` |
| **Java** | 1 `.java` per public class | `.java` | `Robot.java` → `class Robot` |
| **C** | 1 `.h` + 1 `.c` | `.h` + `.c` | `robot.h` + `robot.c` |

---

# 3. The 4 Pillars of OOP

```
         ┌─────────────────────────────────────────────────────┐
         │                  4 PILLARS OF OOP                   │
         │                                                     │
         │  1. ENCAPSULATION   Bundle data + methods together  │
         │                     Hide internal details           │
         │                                                     │
         │  2. INHERITANCE     Build new classes from existing │
         │                     Reuse and extend code           │
         │                                                     │
         │  3. POLYMORPHISM    Same interface, many behaviours │
         │                     One call → different results    │
         │                                                     │
         │  4. ABSTRACTION     Show only what's necessary      │
         │                     Hide complexity behind an API   │
         └─────────────────────────────────────────────────────┘
```

> - **Encapsulation** — wraps related data and functions together, and **hides** internal implementation. Like a TV remote: you press buttons (interface) without knowing the circuit board inside (implementation).
> - **Inheritance** — a new class gains the properties and methods of an existing class. Like a child inheriting traits from parents, then adding their own.
> - **Polymorphism** — from Greek: **poly** = many, **morphos** = form. The same method call behaves differently depending on which object type it's called on.
> - **Abstraction** — exposing only the essential interface while hiding complexity. Like driving a car: you use the steering wheel and pedals (abstraction) without understanding the engine internals.
> - **API** = **A**pplication **P**rogramming **I**nterface. The set of methods/functions a class exposes for others to use.

---

# 4. Classes & Objects

## 🐍 Python

```python
# ── DEFINING A CLASS ─────────────────────────────────────────────
class Robot:
    """A simple robot class — docstring describes the class"""

    # CLASS VARIABLE — shared by ALL instances
    species = "Autonomous Robot"
    count   = 0

    # CONSTRUCTOR — special method called when creating an instance
    def __init__(self, name: str, speed: float):
        # INSTANCE VARIABLES — unique to each object
        self.name  = name
        self.speed = speed
        self.x     = 0.0
        Robot.count += 1


# ── CREATING OBJECTS (INSTANCES) ─────────────────────────────────
r1 = Robot("R2D2",  speed=0.5)
r2 = Robot("C-3PO", speed=0.3)

print(r1.name)          # R2D2
print(Robot.count)      # 2
print(isinstance(r1, Robot))  # True
```

> - `self` — a reference to the **current instance**. Always the first parameter of every instance method. Python passes it automatically.
> - **class variable** — defined at class level (no `self`). Shared across all instances.
> - **instance variable** — created with `self.name = ...`. Each object has its own copy.

---

## ⚙️ C++

```cpp
// Robot.h
#pragma once
#include <string>

class Robot {
public:
    static int count;

    Robot(std::string name, double speed);
    ~Robot();

    std::string getName()  const;
    double      getSpeed() const;
    void        setSpeed(double s);

private:
    std::string name_;
    double      speed_;
    double      x_;
};
```

```cpp
// Robot.cpp
#include "Robot.h"
#include <iostream>

int Robot::count = 0;

Robot::Robot(std::string name, double speed)
    : name_(name), speed_(speed), x_(0.0)
{
    Robot::count++;
    std::cout << "Robot " << name_ << " created.\n";
}

Robot::~Robot() {
    Robot::count--;
    std::cout << "Robot " << name_ << " destroyed.\n";
}

std::string Robot::getName()  const { return name_; }
double      Robot::getSpeed() const { return speed_; }
void        Robot::setSpeed(double s) { if (s >= 0.0) speed_ = s; }
```

```cpp
// main.cpp
#include "Robot.h"
#include <iostream>

int main() {
    Robot r1("R2D2",  0.5);    // stack — auto-destroyed at }
    Robot r2("C-3PO", 0.3);

    Robot* r3 = new Robot("BB-8", 0.7);   // heap — must delete
    std::cout << Robot::count << "\n";    // 3
    delete r3;

    return 0;
}
```

> - **member initializer list** `: name_(name), speed_(speed)` — initialises members before the constructor body runs. More efficient than assigning inside the body.
> - `const` after a method — promises not to modify the object. Required for all getters.
> - **stack allocation** — object auto-destroyed when scope ends.
> - **heap allocation** (`new`) — lives until `delete` is called.
> - `Robot::` — scope resolution operator. Needed outside the class body.

---

## ☕ Java

```java
// Robot.java
package com.myrobot;

public class Robot {
    private static int count = 0;

    private String name;
    private double speed;
    private double x;

    public Robot(String name, double speed) {
        this.name  = name;
        this.speed = speed;
        this.x     = 0.0;
        count++;
    }

    public String getName()  { return name; }
    public double getSpeed() { return speed; }

    public void setSpeed(double s) {
        if (s >= 0.0) this.speed = s;
    }

    public static int getCount() { return count; }

    @Override
    public String toString() {
        return "Robot{name=" + name + ", speed=" + speed + "}";
    }
}
```

```java
// Main.java
package com.myrobot;

public class Main {
    public static void main(String[] args) {
        Robot r1 = new Robot("R2D2",  0.5);
        Robot r2 = new Robot("C-3PO", 0.3);

        System.out.println(r1.getName());       // R2D2
        System.out.println(Robot.getCount());   // 2
        System.out.println(r1);                 // Robot{name=R2D2, speed=0.5}
    }
}
```

> - In Java, **all objects are on the heap**. The GC automatically frees memory.
> - `@Override` — annotation that verifies this method overrides a parent method.
> - `toString()` — called automatically by `System.out.println(obj)`.
> - `this.name` — required when a parameter has the same name as a field.

---

# 5. Attributes — Data Inside a Class

## Types of attributes

```python
# ── PYTHON ────────────────────────────────────────────────────────
class BankAccount:
    interest_rate = 0.05          # CLASS attribute: shared by all accounts

    def __init__(self, owner, balance):
        self.owner   = owner      # INSTANCE attribute: each account has its own
        self.balance = balance
        self._pin    = 1234       # PROTECTED by convention (single _)
        self.__secret = "abc"     # PRIVATE by name mangling (double __)
```

```cpp
// ── C++ — BankAccount.h ───────────────────────────────────────────
class BankAccount {
public:
    static double interest_rate;    // CLASS attribute (static)
    std::string owner;              // INSTANCE attribute

protected:
    double balance;                 // accessible in subclasses

private:
    int    pin_;                    // only inside this class
    std::string secret_;
};
// BankAccount.cpp:
double BankAccount::interest_rate = 0.05;
```

```java
// ── JAVA — BankAccount.java ───────────────────────────────────────
public class BankAccount {
    public  static double interestRate = 0.05;  // CLASS attribute
    public  String owner;
    protected double balance;
    private int    pin;
    private String secret;
}
```

> - **class attribute** (static) — one copy shared by **all** instances.
> - **instance attribute** — one copy **per object**. Independent values.
> - **protected** — accessible in the class **and** subclasses.
> - **private** — only accessible inside the class itself.
> - Python's `_` prefix — a **convention** (not enforced). Signals internal use.
> - Python's `__` prefix — **name mangling**: renamed to `_BankAccount__secret` internally.

---

# 6. Methods — Behaviour Inside a Class

## Types of methods

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Robot:
    robot_count = 0

    def __init__(self, name, speed):
        self.name  = name
        self.speed = speed
        self.x     = 0.0

    # INSTANCE METHOD — operates on self
    def move(self, distance):
        self.x += distance
        return self.x

    # CLASS METHOD — operates on the class
    @classmethod
    def create_fast_robot(cls, name):
        return cls(name, speed=2.0)

    # STATIC METHOD — utility, no self or cls
    @staticmethod
    def speed_to_kmh(speed_ms):
        return speed_ms * 3.6

    # PROPERTY — access method like an attribute
    @property
    def speed_kmh(self):
        return self.speed * 3.6

    @speed_kmh.setter
    def speed_kmh(self, value_kmh):
        self.speed = value_kmh / 3.6
```

```cpp
// ── C++ — Robot.h ─────────────────────────────────────────────────
class Robot {
public:
    void move(double distance);              // instance method
    double getX() const;                     // const: won't modify object
    static double speed_to_kmh(double s);   // static method
    virtual void describe();                 // virtual: can be overridden
    virtual void perform_task() = 0;        // pure virtual: must override
};
```

```java
// ── JAVA — Robot.java ─────────────────────────────────────────────
public class Robot {
    public void move(double distance) { x += distance; }           // instance
    public static double speedToKmh(double s) { return s * 3.6; } // static
    public final void shutdown() { System.out.println("Off"); }    // final: no override
    public void describe() { System.out.println("Robot: " + name); } // virtual by default
}
```

> - `@classmethod` — first param is `cls` (the class). Used for factory methods.
> - `@staticmethod` — utility function. No automatic first parameter.
> - `@property` — turns a method into an attribute-like accessor. Read without `()`.
> - `virtual` (C++) — enables runtime polymorphism via vtable.
> - `= 0` (C++) — makes a method pure virtual → class becomes abstract.
> - In Java, all non-final, non-static methods are virtual by default.
> - `final` (Java) — prevents subclasses from overriding it.

---

# 7. Constructors & Destructors

## Constructor types

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Motor:
    def __init__(self, rpm=0, power=100, name="Motor"):
        self.rpm   = rpm
        self.power = power
        self.name  = name

    def __del__(self):
        print(f"{self.name} destroyed")

m1 = Motor()
m2 = Motor(rpm=1000)
m3 = Motor(500, 80, "M3")
```

```cpp
// ── C++ — Motor.h ─────────────────────────────────────────────────
class Motor {
public:
    Motor();                               // default constructor
    Motor(int rpm, int power, std::string name); // parameterised
    Motor(const Motor& other);            // copy constructor
    Motor(Motor&& other) noexcept;        // move constructor (C++11)
    ~Motor();                             // destructor
private:
    int rpm_, power_;
    std::string name_;
};
```

```cpp
// ── C++ — Motor.cpp ───────────────────────────────────────────────
Motor::Motor()
    : rpm_(0), power_(100), name_("Motor") {}

Motor::Motor(int rpm, int power, std::string name)
    : rpm_(rpm), power_(power), name_(name) {}

Motor::Motor(const Motor& other)
    : rpm_(other.rpm_), power_(other.power_), name_(other.name_) {
    std::cout << "Motor copied\n";
}

Motor::Motor(Motor&& other) noexcept
    : rpm_(other.rpm_), power_(other.power_), name_(std::move(other.name_)) {
    other.rpm_ = 0;
}

Motor::~Motor() {
    std::cout << name_ << " destroyed\n";
}
```

```java
// ── JAVA — Motor.java ─────────────────────────────────────────────
public class Motor {
    private int    rpm, power;
    private String name;

    public Motor() {
        this(0, 100, "Motor");    // constructor chaining
    }

    public Motor(int rpm, int power, String name) {
        this.rpm = rpm; this.power = power; this.name = name;
    }

    public Motor(Motor other) {   // copy constructor — manual in Java
        this.rpm = other.rpm; this.power = other.power; this.name = other.name;
    }
    // Java has no destructor — GC handles memory
}
```

> - **copy constructor** (C++) — `const Motor& other`: creates a new object as a copy. `const` = won't modify the original. `&` = reference.
> - **move constructor** (C++) — `Motor&&`: transfers resources instead of copying. Much faster for large objects.
> - `noexcept` — guarantees no exceptions are thrown. Enables compiler optimisations.
> - `this(...)` (Java) — constructor chaining: must be the **first statement**.
> - **Rule of Five** (C++) — if you define any of destructor/copy ctor/copy assign/move ctor/move assign → define all five.

---

# 8. Access Modifiers — public · private · protected

```
                    Same      Subclass  Outside
                    class     anywhere  class
────────────────────────────────────────────────
Python (convention):
  no prefix         ✅         ✅         ✅     public
  _single           ✅         ✅         ⚠️     protected (convention)
  __double          ✅         ❌         ❌     private (name mangling)

C++:
  public            ✅         ✅         ✅
  protected         ✅         ✅         ❌
  private           ✅         ❌         ❌

Java:
  public            ✅         ✅         ✅
  protected         ✅         ✅         ❌
  (package-private) ✅         ❌         ❌    (no keyword — default)
  private           ✅         ❌         ❌
```

> - **package-private** (Java) — default when no modifier is written. Accessible within the same package only.
> - Python access control is **by convention only** — nothing technically prevents accessing `_private`.
> - `friend` (C++) — a class/function declared `friend` can access private members.

```cpp
// C++ friend example — FriendExample.h
class BankAccount {
    friend class Auditor;
private:
    double balance_ = 1000.0;
};

class Auditor {
public:
    void check(BankAccount& acc) {
        std::cout << acc.balance_;   // ✅ allowed by friend
    }
};
```

---

# 9. Inheritance — Building on Existing Classes

## Single Inheritance

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def breathe(self):
        return f"{self.name} breathes"

    def speak(self):
        return "..."


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self):              # OVERRIDE
        return "Woof!"

    def fetch(self):              # NEW method
        return f"{self.name} fetches"


dog = Dog("Rex", 3, "Labrador")
print(dog.breathe())     # inherited from Animal
print(dog.speak())       # Woof! — overridden
print(isinstance(dog, Animal))  # True — dog IS-A Animal
```

```
// ── C++ — file structure for inheritance ─────────────────────────
my_project/
├── Animal.h        ← base class declaration
├── Animal.cpp      ← base class implementation
├── Dog.h           ← derived class declaration (#include "Animal.h")
├── Dog.cpp         ← derived class implementation (#include "Dog.h")
└── main.cpp        ← (#include "Dog.h")
```

```cpp
// Animal.h
#pragma once
#include <string>

class Animal {
public:
    Animal(std::string name, int age);
    virtual ~Animal();               // ALWAYS virtual destructor
    void breathe() const;
    virtual void speak() const;      // virtual = can be overridden

protected:
    std::string name_;
    int age_;
};
```

```cpp
// Animal.cpp
#include "Animal.h"
#include <iostream>

Animal::Animal(std::string name, int age) : name_(name), age_(age) {}
Animal::~Animal() {}

void Animal::breathe() const { std::cout << name_ << " breathes\n"; }
void Animal::speak()   const { std::cout << "...\n"; }
```

```cpp
// Dog.h
#pragma once
#include "Animal.h"     // always include the parent header

class Dog : public Animal {
public:
    Dog(std::string name, int age, std::string breed);
    void speak() const override;    // override keyword: compiler verifies
    void fetch() const;

private:
    std::string breed_;
};
```

```cpp
// Dog.cpp
#include "Dog.h"
#include <iostream>

Dog::Dog(std::string name, int age, std::string breed)
    : Animal(name, age)             // call parent constructor
    , breed_(breed)
{}

void Dog::speak() const { std::cout << "Woof!\n"; }
void Dog::fetch() const { std::cout << name_ << " fetches!\n"; }
```

```cpp
// main.cpp
#include "Dog.h"
#include <iostream>

int main() {
    Dog dog("Rex", 3, "Labrador");
    dog.breathe();        // inherited
    dog.speak();          // Woof! — overridden

    Animal* a = new Dog("Buddy", 2, "Poodle");  // polymorphism
    a->speak();           // Woof! — dynamic dispatch
    delete a;             // ~Dog() called BECAUSE ~Animal() is virtual

    return 0;
}
```

```java
// ── JAVA — file per class ─────────────────────────────────────────
// Animal.java
package com.myrobot;

public class Animal {
    protected String name;
    protected int    age;

    public Animal(String name, int age) {
        this.name = name; this.age = age;
    }

    public void breathe() { System.out.println(name + " breathes"); }
    public void speak()   { System.out.println("..."); }
}
```

```java
// Dog.java
package com.myrobot;

public class Dog extends Animal {
    private String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);              // MUST be first line
        this.breed = breed;
    }

    @Override
    public void speak() { System.out.println("Woof!"); }

    public void fetch() { System.out.println(name + " fetches!"); }
}
```

> - `super()` — calls the parent constructor. Always call first in child's `__init__` / constructor.
> - `override` (C++) — compiler verifies the method actually overrides a virtual method. Always use it.
> - `virtual ~Animal()` (C++) — **virtual destructor** is the single most critical rule in C++ inheritance. Without it, deleting via base pointer leaks the derived class resources.
> - `extends` (Java) — keyword for inheritance. A class can extend only **one** class.
> - In the C++ file structure, `Dog.h` must `#include "Animal.h"` so the compiler knows what `Animal` is.

## Multiple Inheritance

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Flyable:
    def fly(self): return "Flying!"

class Swimmable:
    def swim(self): return "Swimming!"

class Duck(Flyable, Swimmable):
    def quack(self): return "Quack!"

print(Duck.__mro__)
# Duck → Flyable → Swimmable → object
```

> - **MRO** = **M**ethod **R**esolution **O**rder. Python uses C3 linearisation (left-to-right, depth-first) to decide which parent's method wins.
> - **diamond problem** — when D inherits from B and C, both inheriting from A. Python's MRO resolves this. Java avoids it for classes (only allows single inheritance).

---

# 10. Polymorphism — One Interface Many Behaviours

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Shape:
    def area(self) -> float:
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self): return self.w * self.h

def print_area(shape: Shape):
    print(f"Area: {shape.area():.2f}")  # same call, different behaviour

shapes = [Circle(5), Rectangle(4, 6)]
for s in shapes:
    print_area(s)
```

```
// ── C++ — file structure ──────────────────────────────────────────
shapes/
├── Shape.h         ← abstract base
├── Circle.h        ← (#include "Shape.h")
├── Circle.cpp
├── Rectangle.h     ← (#include "Shape.h")
├── Rectangle.cpp
└── main.cpp        ← (#include "Circle.h", "Rectangle.h")
```

```cpp
// Shape.h
#pragma once

class Shape {
public:
    virtual double area() const = 0;  // pure virtual
    virtual ~Shape() {}
};
```

```cpp
// Circle.h
#pragma once
#include "Shape.h"

class Circle : public Shape {
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
private:
    double r_;
};
```

```cpp
// main.cpp
#include "Circle.h"
#include "Rectangle.h"
#include <vector>
#include <memory>

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));

    for (const auto& s : shapes) {
        std::cout << "Area: " << s->area() << "\n";
    }
}
```

> - `std::unique_ptr<Shape>` — smart pointer. Owns the object exclusively. Auto-deletes when out of scope.
> - `std::make_unique<Circle>(5.0)` — preferred over `new Circle(5.0)`. Exception-safe.
> - `const auto&` — deduces type, const reference, no copy.

---

# 11. Abstract Classes & Interfaces

```python
# ── PYTHON ────────────────────────────────────────────────────────
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def move(self): pass

    @abstractmethod
    def fuel_type(self) -> str: pass

    def describe(self):
        return f"{self.brand}: {self.fuel_type()}"

class ElectricCar(Vehicle):
    def move(self):       return "Driving silently"
    def fuel_type(self):  return "Electric"

# v = Vehicle("X")     # ❌ TypeError: Can't instantiate abstract class
car = ElectricCar("Tesla")
print(car.describe())   # Tesla: Electric
```

```java
// ── JAVA — IMoveable.java (interface) ─────────────────────────────
package com.myrobot;

public interface IMoveable {
    void accelerate(double amount);     // implicitly public abstract
    void brake();
    double getSpeed();

    default void horn() {               // default method (Java 8+)
        System.out.println("Beep!");
    }

    double MAX_SPEED = 200.0;           // implicitly public static final
}
```

```java
// Tesla.java — implements multiple interfaces
package com.myrobot;

public class Tesla extends Vehicle implements IMoveable, IElectric {
    private double speed   = 0;
    private int    battery = 100;

    @Override public void   accelerate(double a) { speed += a; }
    @Override public void   brake()              { speed -= 10; }
    @Override public double getSpeed()           { return speed; }
    @Override public int    getBatteryPercent()  { return battery; }
    @Override public void   charge()             { battery = 100; }
}
```

```cpp
// ── C++ — IMoveable.h (abstract class as interface) ───────────────
#pragma once

class IMoveable {
public:
    virtual void   accelerate(double amount) = 0;
    virtual void   brake()                  = 0;
    virtual double getSpeed() const         = 0;
    virtual ~IMoveable() {}
};
```

```cpp
// Tesla.h
#pragma once
#include "IMoveable.h"
#include "IElectric.h"

class Tesla : public IMoveable, public IElectric {
public:
    void   accelerate(double a) override { speed_ += a; }
    void   brake()              override { speed_ -= 10; }
    double getSpeed() const     override { return speed_; }
    int    getBatteryPercent() const override { return battery_; }
    void   charge()             override { battery_ = 100; }

private:
    double speed_   = 0.0;
    int    battery_ = 100;
};
```

> - `ABC` — **A**bstract **B**ase **C**lass. Makes the class abstract in Python.
> - `@abstractmethod` — method must be overridden in concrete subclasses.
> - `interface` (Java) — pure contract. A class can `implements` many interfaces.
> - `default method` (Java 8+) — interface method with implementation.
> - In C++, interface = abstract class. Convention: prefix with `I` (`IMoveable`).
> - In C++, each interface gets its own `.h` file.

---

# 12. Static Members

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Config:
    MAX_SPEED    = 2.0
    DEFAULT_NAME = "Robot"

    @staticmethod
    def validate_speed(speed):
        return 0.0 <= speed <= Config.MAX_SPEED
```

```cpp
// ── C++ — Config.h ────────────────────────────────────────────────
#pragma once
#include <string>

class Config {
public:
    static constexpr double MAX_SPEED  = 2.0;
    static constexpr int    MAX_ROBOTS = 100;
    static const std::string DEFAULT_NAME;   // defined in .cpp

    static bool validate_speed(double s);
    static int  get_robot_count();

private:
    static int robot_count_;
};
```

```cpp
// Config.cpp
#include "Config.h"

const std::string Config::DEFAULT_NAME = "Robot";
int               Config::robot_count_ = 0;

bool Config::validate_speed(double s) {
    return s >= 0.0 && s <= MAX_SPEED;
}

int Config::get_robot_count() { return robot_count_; }
```

```java
// Config.java
public class Config {
    public  static final double MAX_SPEED  = 2.0;
    public  static final int    MAX_ROBOTS = 100;
    private static       int    robotCount = 0;

    public static boolean validateSpeed(double s) {
        return s >= 0.0 && s <= MAX_SPEED;
    }
}
```

> - `constexpr` (C++) — evaluated at **compile time**. The fastest constant.
> - `static final` (Java) — class-level constant. Cannot be reassigned.
> - Static members must be **declared** in the `.h` and **defined** in the `.cpp` for C++.
> - **Utility class** — only static methods and constants. Never instantiated.

---

# 13. Special Methods & Operator Overloading

## Python Dunder Methods

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x; self.y = y

    def __str__(self):      return f"Vector({self.x}, {self.y})"
    def __repr__(self):     return f"Vector2D(x={self.x}, y={self.y})"
    def __add__(self, o):   return Vector2D(self.x + o.x, self.y + o.y)
    def __sub__(self, o):   return Vector2D(self.x - o.x, self.y - o.y)
    def __mul__(self, s):   return Vector2D(self.x * s,   self.y * s)
    def __rmul__(self, s):  return self.__mul__(s)
    def __neg__(self):      return Vector2D(-self.x, -self.y)
    def __abs__(self):
        import math; return math.sqrt(self.x**2 + self.y**2)
    def __eq__(self, o):    return self.x == o.x and self.y == o.y
    def __len__(self):      return 2
    def __getitem__(self, i):
        if i == 0: return self.x
        if i == 1: return self.y
        raise IndexError("out of range")
    def __iter__(self):
        yield self.x; yield self.y
    def __call__(self, scale):
        return self * scale

v1, v2 = Vector2D(1, 2), Vector2D(3, 4)
print(v1 + v2)     # Vector(4, 6)
print(3 * v1)      # Vector(3, 6)    ← __rmul__
print(v1[0])       # 1               ← __getitem__
print(v1(5))       # Vector(5, 10)   ← __call__
```

> - **dunder** = **d**ouble **under**score. Called automatically by Python operators.
> - `__rmul__` — the **reflected** version: `3 * v1` tries `int.__mul__(v1)` first, then falls back to `v1.__rmul__(3)`.
> - `__call__` — makes an object callable: `obj(args)`.
> - `yield` — makes `__iter__` a **generator**: pauses and returns values one at a time.

## C++ Operator Overloading

```cpp
// Vector2D.h
#pragma once
#include <ostream>

class Vector2D {
public:
    double x, y;

    Vector2D(double x, double y) : x(x), y(y) {}

    Vector2D  operator+(const Vector2D& o) const { return {x+o.x, y+o.y}; }
    Vector2D  operator-(const Vector2D& o) const { return {x-o.x, y-o.y}; }
    Vector2D  operator*(double s)          const { return {x*s,   y*s};   }
    Vector2D  operator-()                  const { return {-x, -y}; }
    Vector2D& operator+=(const Vector2D& o) { x+=o.x; y+=o.y; return *this; }
    bool      operator==(const Vector2D& o) const { return x==o.x && y==o.y; }
    bool      operator<(const Vector2D& o)  const;
    double&   operator[](int i);
    double    magnitude() const;

    // Free function declarations (defined in .cpp or inline below)
    friend Vector2D     operator*(double s, const Vector2D& v);
    friend std::ostream& operator<<(std::ostream& os, const Vector2D& v);
};
```

```cpp
// Vector2D.cpp
#include "Vector2D.h"
#include <cmath>
#include <stdexcept>

double Vector2D::magnitude() const { return std::sqrt(x*x + y*y); }

bool Vector2D::operator<(const Vector2D& o) const {
    return magnitude() < o.magnitude();
}

double& Vector2D::operator[](int i) {
    if (i == 0) return x;
    if (i == 1) return y;
    throw std::out_of_range("Vector2D: index out of range");
}

// Free functions
Vector2D operator*(double s, const Vector2D& v) {
    return {s * v.x, s * v.y};
}

std::ostream& operator<<(std::ostream& os, const Vector2D& v) {
    return os << "Vector(" << v.x << ", " << v.y << ")";
}
```

> - `return *this` — returns reference to the current object. Enables chaining: `v1 += v2 += v3`.
> - **free function** operators — when the left operand isn't your class (e.g. `3.0 * v`), write a free function outside the class, declared as `friend` to access private members.
> - `operator<<` — the **stream output operator**. Returns `ostream&` for chaining.
> - Note the split: declarations go in `.h`, implementations in `.cpp`.

---

# 14. Templates & Generics

## C++ Templates

```cpp
// Stack.h — templates MUST be fully defined in the header
// (the compiler needs the full definition at each use site)
#pragma once
#include <stdexcept>

template <typename T, int Capacity = 10>
class Stack {
public:
    void push(const T& item) {
        if (size_ < Capacity) data_[size_++] = item;
    }

    T pop() {
        if (size_ == 0) throw std::underflow_error("Stack is empty");
        return data_[--size_];
    }

    T&   top()   { return data_[size_ - 1]; }
    bool empty() const { return size_ == 0; }
    int  size()  const { return size_; }

private:
    T   data_[Capacity];
    int size_ = 0;
};

// Function template
template <typename T>
T maximum(T a, T b) { return (a > b) ? a : b; }
```

```cpp
// main.cpp
#include "Stack.h"

int main() {
    Stack<int>         int_stack;
    Stack<std::string> str_stack;
    Stack<double, 50>  big_stack;

    int_stack.push(1);
    int_stack.push(2);
    std::cout << int_stack.pop() << "\n";  // 2
}
```

> - **Templates must be in the header** (`.h` or `.hpp`). The compiler generates a separate class for each type used — it needs the full definition at compile time. Unlike regular classes, there is **no `.cpp` file** for template classes.
> - **Template instantiation** — `Stack<int>` and `Stack<double>` are completely separate classes generated by the compiler.
> - `constexpr` non-type parameter (`int Capacity`) — a compile-time integer parameter.

## Java Generics

```java
// Stack.java
public class Stack<T> {
    private Object[] data;
    private int size = 0;
    private int capacity;

    @SuppressWarnings("unchecked")
    public Stack(int capacity) {
        this.capacity = capacity;
        data = new Object[capacity];
    }

    public void push(T item) {
        if (size < capacity) data[size++] = item;
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        if (size == 0) throw new RuntimeException("Stack empty");
        return (T) data[--size];
    }
}

// SortedList.java — bounded type parameter
public class SortedList<T extends Comparable<T>> {
    public T findMin(java.util.List<T> list) {
        T min = list.get(0);
        for (T item : list)
            if (item.compareTo(min) < 0) min = item;
        return min;
    }
}
```

> - **Type erasure** — Java generics are compile-time only. At runtime, the JVM sees `Object`. That's why the internal array must be `Object[]`.
> - `T extends Comparable<T>` — bounded type parameter: only types implementing `Comparable` allowed.
> - Unlike C++ templates, Java generics have **one class file** — no code duplication per type.

## Python Generics (Type Hints)

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data: raise IndexError("Stack is empty")
        return self._data.pop()

int_stack: Stack[int] = Stack()
int_stack.push(42)
print(int_stack.pop())   # 42
```

> - Python generics are **type-hint only** — not enforced at runtime. Tools like `mypy` use them for static analysis.

---

# 15. Memory Management

```
Language    Memory management     You manage?   Crashes possible?
──────────────────────────────────────────────────────────────────
C           Manual (malloc/free)  ✅ Yes        ✅ Yes
C++         Manual + Smart ptrs   Mostly no     ⚠️ If using raw pointers
Python      Garbage Collector      ❌ No         ❌ No
Java        Garbage Collector      ❌ No         ❌ No
```

## C++ Smart Pointers

```cpp
// SmartPointerDemo.cpp
#include <memory>

{   // unique_ptr — single exclusive owner
    auto r = std::make_unique<Robot>("R2D2", 0.5);
    r->move(1.0);
}   // Robot auto-deleted here

{   // shared_ptr — shared ownership (reference counting)
    auto r1 = std::make_shared<Robot>("C-3PO", 0.3);
    auto r2 = r1;     // ref count = 2
    r1.reset();       // ref count = 1
}   // r2 goes out — count = 0 — Robot deleted

{   // weak_ptr — observe without owning
    std::weak_ptr<Robot> w;
    {
        auto r = std::make_shared<Robot>("BB-8", 0.7);
        w = r;
        if (auto locked = w.lock())
            locked->move(1.0);
    }   // r destroyed — w is now expired
}
```

> - `unique_ptr` — exclusive ownership. Zero overhead vs raw pointer. Cannot be copied, only moved.
> - `shared_ptr` — shared ownership via reference counting. Slightly slower.
> - `weak_ptr` — non-owning observer. Breaks **circular references**.
> - **RAII** — Resource Acquisition Is Initialisation. Smart pointers implement RAII: resource acquired on construction, released on destruction.

---

# 16. OOP in C — Simulating with Structs

```
my_project/
├── main.c
├── robot.h          ← struct + function declarations
└── robot.c          ← function implementations
```

```c
// robot.h
#ifndef ROBOT_H
#define ROBOT_H

typedef struct Robot Robot;

struct Robot {
    char   name[50];
    double speed;
    double x;

    // Function pointers simulate methods
    void   (*move)(Robot* self, double distance);
    void   (*stop)(Robot* self);
    double (*get_x)(const Robot* self);
};

Robot* Robot_new(const char* name, double speed);
void   Robot_delete(Robot* r);

#endif
```

```c
// robot.c
#include "robot.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static void robot_move(Robot* self, double d) {
    self->x += d;
    printf("%s moved to x=%.2f\n", self->name, self->x);
}

static void robot_stop(Robot* self) { self->speed = 0.0; }
static double robot_get_x(const Robot* self) { return self->x; }

Robot* Robot_new(const char* name, double speed) {
    Robot* r = (Robot*)malloc(sizeof(Robot));
    if (!r) return NULL;
    strncpy(r->name, name, 49);
    r->name[49] = '\0';
    r->speed = speed;
    r->x     = 0.0;
    r->move  = robot_move;    // bind function to function pointer
    r->stop  = robot_stop;
    r->get_x = robot_get_x;
    return r;
}

void Robot_delete(Robot* r) { free(r); }
```

```c
// main.c
#include "robot.h"
#include <stdio.h>

int main(void) {
    Robot* r = Robot_new("R2D2", 0.5);
    r->move(r, 1.5);           // must pass r manually (no implicit this)
    printf("x = %.2f\n", r->get_x(r));
    Robot_delete(r);
    return 0;
}
```

> - `static void robot_move` — the `static` keyword on a function in a `.c` file makes it **file-private** (not visible to other `.c` files). Equivalent of `private` in OOP. Good practice for internal helper functions.
> - `->` — accesses struct member **through a pointer**: `r->name` = `(*r).name`.
> - `malloc` / `free` — manual heap allocation. Every `malloc` must have exactly one matching `free`.
> - **struct embedding** for inheritance — place the parent struct as the **first member** of the child struct. A pointer to the child can be safely cast to a pointer to the parent.

---

# 17. Design Patterns

## Singleton

```python
# Python
class RobotConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.speed = 0.5
        return cls._instance

c1 = RobotConfig()
c2 = RobotConfig()
print(c1 is c2)   # True
```

```cpp
// RobotConfig.h
#pragma once

class RobotConfig {
public:
    static RobotConfig& getInstance() {
        static RobotConfig instance;   // created once, thread-safe C++11
        return instance;
    }

    double speed = 0.5;
    bool   debug = false;

private:
    RobotConfig() {}
    RobotConfig(const RobotConfig&) = delete;
    void operator=(const RobotConfig&) = delete;
};
```

> - **Singleton** — ensures only **one instance** of a class exists.
> - `static local variable` (C++) — initialised exactly once. Thread-safe since C++11.
> - `= delete` — disables copy constructor and assignment operator.

## Observer

```python
# Python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

class Robot(EventEmitter):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.speed = 0.0

    def set_speed(self, speed):
        old = self.speed
        self.speed = speed
        self.emit('speed_changed', old_speed=old, new_speed=speed)

robot = Robot("R2D2")
robot.on('speed_changed', lambda old, new: print(f"Speed: {old} → {new}"))
robot.set_speed(0.5)   # Speed: 0.0 → 0.5
```

## Factory

```python
# Python
class RobotFactory:
    @staticmethod
    def create(robot_type: str):
        registry = {
            'drone':  DroneRobot,
            'wheel':  WheelRobot,
            'arm':    ArmRobot,
        }
        if robot_type not in registry:
            raise ValueError(f"Unknown type: {robot_type}")
        return registry[robot_type]()

r = RobotFactory.create('drone')
```

---

# 18. Full Robot Class Example — All 4 Languages

## 🐍 Python

```
robot_project/
├── main.py
├── robot/
│   ├── __init__.py
│   ├── base.py          ← Robot abstract class
│   ├── ground_robot.py  ← GroundRobot
│   └── drone_robot.py   ← DroneRobot
```

```python
# robot/base.py
from abc import ABC, abstractmethod
import math

class Robot(ABC):
    _total = 0

    def __init__(self, name: str, speed: float, x=0.0, y=0.0):
        self._name  = name
        self._speed = speed
        self._x, self._y = x, y
        Robot._total += 1

    @abstractmethod
    def perform_task(self) -> str: pass

    def move_to(self, tx, ty):
        dist = math.sqrt((tx-self._x)**2 + (ty-self._y)**2)
        self._x, self._y = tx, ty
        return dist

    @property
    def position(self): return (self._x, self._y)

    @staticmethod
    def get_total(): return Robot._total

    def __str__(self):
        return f"{self.__class__.__name__}({self._name}) at {self.position}"
```

```python
# robot/ground_robot.py
import math
from .base import Robot

class GroundRobot(Robot):
    def __init__(self, name, speed, wheel_radius=0.05):
        super().__init__(name, speed)
        self._wheel_radius = wheel_radius

    def perform_task(self):
        return f"{self._name} rolling on ground"

    def calculate_rpm(self):
        circ = 2 * math.pi * self._wheel_radius
        return (self._speed / circ) * 60
```

```python
# main.py
from robot.ground_robot import GroundRobot
from robot.drone_robot  import DroneRobot

ground = GroundRobot("Rover", 0.5)
drone  = DroneRobot("Eagle", 2.0, max_altitude=100.0)

for r in [ground, drone]:
    print(r.perform_task())
    r.move_to(1.0, 2.0)
    print(r)

print(f"Total robots: {GroundRobot.get_total()}")
```

---

## ⚙️ C++

```
robot_project/
├── CMakeLists.txt
├── main.cpp
├── include/
│   ├── Robot.h
│   ├── GroundRobot.h
│   └── DroneRobot.h
└── src/
    ├── Robot.cpp
    ├── GroundRobot.cpp
    └── DroneRobot.cpp
```

```cpp
// include/Robot.h
#pragma once
#include <string>

class Robot {
public:
    static int total;

    Robot(std::string name, double speed, double x=0, double y=0);
    virtual ~Robot();

    virtual std::string perform_task() const = 0;
    double move_to(double tx, double ty);

    std::string get_name()  const { return name_; }
    static int  get_total()       { return total; }

    virtual void print() const;

protected:
    std::string name_;
    double speed_, x_, y_;
};
```

```cpp
// src/Robot.cpp
#include "Robot.h"
#include <iostream>
#include <cmath>

int Robot::total = 0;

Robot::Robot(std::string name, double speed, double x, double y)
    : name_(name), speed_(speed), x_(x), y_(y) { ++total; }

Robot::~Robot() { --total; }

double Robot::move_to(double tx, double ty) {
    double dist = std::hypot(tx-x_, ty-y_);
    x_ = tx; y_ = ty;
    return dist;
}

void Robot::print() const {
    std::cout << name_ << " at (" << x_ << ", " << y_ << ")\n";
}
```

```cpp
// include/GroundRobot.h
#pragma once
#include "Robot.h"

class GroundRobot : public Robot {
public:
    GroundRobot(std::string name, double speed, double wheel_r=0.05);
    std::string perform_task() const override;
    double calculate_rpm() const;

private:
    double wheel_radius_;
};
```

```cpp
// src/GroundRobot.cpp
#include "GroundRobot.h"
#include <cmath>

GroundRobot::GroundRobot(std::string name, double speed, double wheel_r)
    : Robot(name, speed), wheel_radius_(wheel_r) {}

std::string GroundRobot::perform_task() const {
    return name_ + " rolling on ground";
}

double GroundRobot::calculate_rpm() const {
    double circ = 2 * M_PI * wheel_radius_;
    return (speed_ / circ) * 60.0;
}
```

```cpp
// main.cpp
#include "GroundRobot.h"
#include "DroneRobot.h"
#include <vector>
#include <memory>
#include <iostream>

int main() {
    std::vector<std::unique_ptr<Robot>> robots;
    robots.push_back(std::make_unique<GroundRobot>("Rover", 0.5));
    robots.push_back(std::make_unique<DroneRobot>("Eagle", 2.0, 100.0));

    for (auto& r : robots) {
        std::cout << r->perform_task() << "\n";
        r->move_to(1.0, 2.0);
        r->print();
    }
    std::cout << "Total: " << Robot::get_total() << "\n";
    return 0;
}
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(RobotProject)
set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(robot_app
    main.cpp
    src/Robot.cpp
    src/GroundRobot.cpp
    src/DroneRobot.cpp
)
```

---

## ☕ Java

```
robot_project/
└── src/main/java/com/myrobot/
    ├── Main.java
    ├── Robot.java
    ├── GroundRobot.java
    └── DroneRobot.java
```

```java
// Robot.java
package com.myrobot;
import java.util.*;

public abstract class Robot {
    private static int total = 0;
    protected String name;
    protected double speed, x, y;

    public Robot(String name, double speed) {
        this.name = name; this.speed = speed; total++;
    }

    public abstract String performTask();

    public double moveTo(double tx, double ty) {
        double dist = Math.hypot(tx-x, ty-y);
        this.x = tx; this.y = ty;
        return dist;
    }

    public String getName()       { return name; }
    public static int getTotal()  { return total; }

    @Override
    public String toString() {
        return getClass().getSimpleName()+"("+name+") at ("+x+", "+y+")";
    }
}
```

```java
// GroundRobot.java
package com.myrobot;

public class GroundRobot extends Robot {
    private double wheelRadius;

    public GroundRobot(String name, double speed, double wheelRadius) {
        super(name, speed);
        this.wheelRadius = wheelRadius;
    }

    @Override
    public String performTask() { return name + " rolling on ground"; }

    public double calculateRpm() {
        double circ = 2 * Math.PI * wheelRadius;
        return (speed / circ) * 60;
    }
}
```

```java
// Main.java
package com.myrobot;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Robot> robots = new ArrayList<>();
        robots.add(new GroundRobot("Rover", 0.5, 0.05));
        robots.add(new DroneRobot("Eagle", 2.0, 100.0));

        for (Robot r : robots) {
            System.out.println(r.performTask());
            r.moveTo(1.0, 2.0);
            System.out.println(r);
        }
        System.out.println("Total: " + Robot.getTotal());
    }
}
```

---

# 19. Language Comparison Cheat Sheet

## Core OOP syntax

| Concept | Python | C++ | Java | C (simulated) |
|---|---|---|---|---|
| Define class | `class X:` | `class X { };` | `public class X { }` | `typedef struct X X;` |
| Inherit | `class X(Y):` | `class X : public Y` | `class X extends Y` | struct embedding |
| Abstract class | `class X(ABC)` | class with `= 0` | `abstract class X` | N/A |
| Interface | duck typing / `ABC` | abstract class | `interface X` | function pointers |
| Implement interface | `class X(I):` | `class X : public I` | `class X implements I` | N/A |
| Constructor | `def __init__` | `X()` | `public X()` | `X_new()` function |
| Destructor | `def __del__` | `~X()` | GC (no destructor) | `X_delete()` function |
| `self` / `this` | `self` (explicit) | `this` (implicit) | `this` (implicit) | pointer (manual) |
| Call parent | `super().__init__()` | `: Y(args)` | `super()` | `Y_init((Y*)self)` |
| Public | (default) | `public:` | `public` | (default in struct) |
| Private | `__prefix` | `private:` | `private` | N/A |
| Protected | `_prefix` | `protected:` | `protected` | N/A |
| Override | `def method(self)` | `override` keyword | `@Override` | replace function ptr |
| Virtual method | all methods | `virtual` keyword | all methods | function pointer |
|
