# 🏗️ Object-Oriented Programming — Complete Guide
> **C · C++ · Python · Java**
> Every concept, keyword, and mechanism explained from scratch 🐚

---

# 📑 Table of Contents

1. [What is OOP and Why it Exists](#1-what-is-oop-and-why-it-exists)
2. [The 4 Pillars of OOP](#2-the-4-pillars-of-oop)
3. [Classes & Objects](#3-classes--objects)
4. [Attributes — Data Inside a Class](#4-attributes--data-inside-a-class)
5. [Methods — Behaviour Inside a Class](#5-methods--behaviour-inside-a-class)
6. [Constructors & Destructors](#6-constructors--destructors)
7. [Access Modifiers — public · private · protected](#7-access-modifiers--public--private--protected)
8. [Inheritance — Building on Existing Classes](#8-inheritance--building-on-existing-classes)
9. [Polymorphism — One Interface Many Behaviours](#9-polymorphism--one-interface-many-behaviours)
10. [Abstract Classes & Interfaces](#10-abstract-classes--interfaces)
11. [Static Members](#11-static-members)
12. [Special Methods & Operator Overloading](#12-special-methods--operator-overloading)
13. [Templates & Generics](#13-templates--generics)
14. [Memory Management](#14-memory-management)
15. [OOP in C — Simulating with Structs](#15-oop-in-c--simulating-with-structs)
16. [Design Patterns](#16-design-patterns)
17. [Full Robot Class Example — All 4 Languages](#17-full-robot-class-example--all-4-languages)
18. [Language Comparison Cheat Sheet](#18-language-comparison-cheat-sheet)

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

# 2. The 4 Pillars of OOP

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

# 3. Classes & Objects

## 🐍 Python

```python
# ── DEFINING A CLASS ─────────────────────────────────────────────
class Robot:
    """A simple robot class — docstring describes the class"""
    # A docstring is a string literal at the start of a class/function
    # Accessible via Robot.__doc__

    # CLASS VARIABLE — shared by ALL instances
    # (like a static member in other languages)
    species = "Autonomous Robot"
    count   = 0               # tracks how many Robot objects exist

    # CONSTRUCTOR — special method called when creating an instance
    def __init__(self, name: str, speed: float):
        # INSTANCE VARIABLES — unique to each object
        self.name  = name     # every robot has its own name
        self.speed = speed    # every robot has its own speed
        self.x     = 0.0     # initialised to 0 for everyone

        Robot.count += 1      # increment the shared counter


# ── CREATING OBJECTS (INSTANCES) ─────────────────────────────────
r1 = Robot("R2D2",  speed=0.5)   # create instance 1
r2 = Robot("C-3PO", speed=0.3)   # create instance 2

# ── ACCESSING ATTRIBUTES ─────────────────────────────────────────
print(r1.name)          # R2D2
print(r2.speed)         # 0.3
print(Robot.species)    # Autonomous Robot (class variable)
print(Robot.count)      # 2 (both instances share this)

# ── TYPE CHECKING ─────────────────────────────────────────────────
print(type(r1))            # <class '__main__.Robot'>
print(isinstance(r1, Robot))  # True
```

> - `class Robot:` — defines a **class**. By convention, class names use **PascalCase** (each word capitalised, no underscores).
> - `"""docstring"""` — a string literal immediately after `class`/`def`. Python's built-in documentation system. Access with `ClassName.__doc__`.
> - `def __init__(self, ...)` — the **constructor**. The double underscores `__` make it a **dunder** (double under) method — a special Python method. Runs automatically when you call `Robot(...)`.
> - `self` — a reference to the **current instance**. It's always the **first parameter** of every instance method. Python passes it automatically — you never write `r1.method(r1)`.
> - **instance variable** — created with `self.name = ...`. Each object has its own copy.
> - **class variable** — defined at class level (no `self`). **Shared** across all instances. Changing it changes it for everyone.
> - `isinstance(obj, Class)` — checks if an object is an instance of a class (or a subclass of it).

---

## ⚙️ C++

```cpp
#include <iostream>
#include <string>

// ── DEFINING A CLASS ─────────────────────────────────────────────
class Robot {
    // Everything is private by default in a class
    // (opposite of struct, where everything is public by default)

public:    // ← access specifier: below is accessible from outside

    // STATIC member variable — shared by all instances
    static int count;         // declared here
    // (defined outside the class — see below)

    // CONSTRUCTOR — same name as class, no return type
    Robot(std::string name, double speed)
        : name_(name), speed_(speed), x_(0.0)
        // ↑ member initializer list: initialises members before body runs
        // More efficient than assigning inside the body
    {
        Robot::count++;      // Robot:: = access class-level member
        std::cout << "Robot " << name_ << " created.\n";
    }

    // DESTRUCTOR — called when the object is destroyed
    ~Robot() {
        Robot::count--;
        std::cout << "Robot " << name_ << " destroyed.\n";
    }

    // GETTER METHODS — read private data safely
    std::string getName()  const { return name_; }
    double      getSpeed() const { return speed_; }
    double      getX()     const { return x_; }

    // SETTER METHOD — write private data with validation
    void setSpeed(double s) {
        if (s >= 0.0) speed_ = s;    // validate before setting
    }

private:   // ← private: not accessible from outside the class

    // MEMBER VARIABLES — trailing _ is a common C++ naming convention
    std::string name_;
    double      speed_;
    double      x_;
};

// ── DEFINE the static member outside the class ───────────────────
int Robot::count = 0;
// Static members must be defined exactly ONCE outside the class
// (the class declaration only DECLARES them, not defines)


// ── CREATING OBJECTS ─────────────────────────────────────────────
int main() {

    // Stack allocation — object lives until } closes
    Robot r1("R2D2",  0.5);
    Robot r2("C-3PO", 0.3);

    // Heap allocation — must manually delete (or use smart pointer)
    Robot* r3 = new Robot("BB-8", 0.7);

    // Accessing members
    std::cout << r1.getName()  << "\n";   // R2D2
    std::cout << r2.getSpeed() << "\n";   // 0.3
    std::cout << Robot::count  << "\n";   // 3

    delete r3;   // free heap memory — destructor called here
    // r1, r2 destroyed automatically when main() ends

    return 0;
}
```

> - `class` vs `struct` in C++ — the **only** difference is the **default access**: `class` defaults to `private`, `struct` defaults to `public`. Conventionally: `class` for OOP objects, `struct` for plain data.
> - **member initializer list** `: name_(name), speed_(speed)` — initialises member variables **before** the constructor body `{}` runs. More efficient than `name_ = name` inside the body, especially for non-trivial types.
> - `const` after a method — `std::string getName() const` — means this method **promises not to modify** the object. You can call it on `const` objects. Good practice for all getters.
> - `~Robot()` — the **destructor**. Called automatically when an object goes out of scope (stack) or is `delete`d (heap). No return type, no parameters.
> - **stack allocation** (`Robot r1(...)`) — object created on the stack. Automatically destroyed when scope ends. Fast, no manual cleanup needed.
> - **heap allocation** (`new Robot(...)`) — object created on the heap. Lives until `delete` is called. Needed when the object must outlive its scope or size is unknown at compile time.
> - `static int count` — must be **declared** inside the class AND **defined** outside (`int Robot::count = 0`). The `::` is the **scope resolution operator**.

---

## ☕ Java

```java
// ── DEFINING A CLASS ─────────────────────────────────────────────
// In Java: ONE public class per file, filename MUST match class name
// File: Robot.java

public class Robot {
    // public = accessible everywhere
    // class  = keyword to define a class

    // STATIC FIELD — shared by all instances
    private static int count = 0;
    // private static: hidden from outside but shared across all instances

    // INSTANCE FIELDS — unique to each object
    private String name;     // String is a class in Java (not a primitive)
    private double speed;    // double is a primitive type
    private double x;

    // CONSTRUCTOR — same name as class, no return type
    public Robot(String name, double speed) {
        this.name  = name;    // this.name = instance field
        this.speed = speed;   // name (right side) = constructor parameter
        this.x     = 0.0;
        count++;              // no this. needed for static — just count++
    }

    // GETTERS & SETTERS (Java convention: getX() / setX())
    public String getName()  { return name; }
    public double getSpeed() { return speed; }

    public void setSpeed(double s) {
        if (s >= 0.0) this.speed = s;
    }

    // Static method — called on the class, not an instance
    public static int getCount() { return count; }

    // toString() — Java calls this automatically for print/debug
    @Override
    public String toString() {
        return "Robot{name=" + name + ", speed=" + speed + "}";
    }
    // @Override = annotation: signals this method overrides a parent method
}


// ── CREATING OBJECTS ─────────────────────────────────────────────
public class Main {
    public static void main(String[] args) {

        // In Java ALL objects live on the heap (no stack allocation)
        Robot r1 = new Robot("R2D2",  0.5);
        Robot r2 = new Robot("C-3PO", 0.3);

        System.out.println(r1.getName());       // R2D2
        System.out.println(r2.getSpeed());      // 0.3
        System.out.println(Robot.getCount());   // 2

        System.out.println(r1);   // Robot{name=R2D2, speed=0.5}
        // ↑ Java automatically calls r1.toString()
    }
}
```

> - `public class Robot` — `public` = accessible from any package. Every Java program entry point needs `public static void main(String[] args)`.
> - `this.name` — refers to the **instance field**. In Java, `this.` is optional when there's no naming conflict, but required when a parameter has the same name as a field (the constructor case above).
> - **In Java, all objects are on the heap**. There's no stack allocation. Java's **Garbage Collector (GC)** automatically frees memory when no references to an object remain — no `delete` needed.
> - `@Override` — an **annotation** (metadata). Tells the compiler "this method intentionally overrides a method from a parent class." The compiler then verifies this — if the method doesn't actually override anything, it gives an error. Good practice.
> - `toString()` — Java's equivalent of Python's `__str__`. Called automatically by `System.out.println(obj)`.
> - **Primitive types** (`int`, `double`, `boolean`, `char`, `long`, `float`) — not objects. Stored by value. Their object wrappers (`Integer`, `Double`, `Boolean`) are actual classes.
> - **String in Java** — `String` is a **class**, not a primitive. But Java treats it specially: string literals (`"hello"`) create `String` objects automatically.

---

# 4. Attributes — Data Inside a Class

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
// ── C++ ───────────────────────────────────────────────────────────
class BankAccount {
public:
    static double interest_rate;    // CLASS attribute (static)
    std::string owner;              // INSTANCE attribute (public — rarely done)

protected:
    double balance;                 // PROTECTED: accessible in subclasses

private:
    int    pin_;                    // PRIVATE: only inside this class
    std::string secret_;
};
double BankAccount::interest_rate = 0.05;   // define static outside class
```

```java
// ── JAVA ──────────────────────────────────────────────────────────
public class BankAccount {
    public  static double interestRate = 0.05;  // CLASS attribute
    public  String owner;                        // rarely public in Java
    protected double balance;                    // accessible in subclasses
    private int    pin;                          // only in this class
    private String secret;
}
```

> - **class attribute** (static) — one copy shared by **all** instances. Changing it changes it for every object. Good for: counters, constants, configuration.
> - **instance attribute** — one copy **per object**. Each object has its own independent value. Good for: object-specific data (name, speed, position).
> - **protected** — accessible inside the class **and** in subclasses (classes that inherit from it). Not accessible from outside.
> - **private** — only accessible inside the class itself. The strictest encapsulation.
> - Python's `_` prefix — a **convention** (not enforced). Signals "this is internal, don't use it directly outside the class." Python doesn't actually block access.
> - Python's `__` prefix — **name mangling**: Python renames `__secret` to `_BankAccount__secret` internally. Still accessible but harder to accidentally use.

---

# 5. Methods — Behaviour Inside a Class

## Types of methods

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Robot:

    robot_count = 0

    def __init__(self, name, speed):
        self.name  = name
        self.speed = speed

    # ── INSTANCE METHOD — operates on self (one specific object) ──
    def move(self, distance):
        """Move the robot forward — needs 'self' to access instance data"""
        self.x += distance
        return self.x
    # Called as: robot.move(1.0)

    # ── CLASS METHOD — operates on the class, not an instance ─────
    @classmethod
    def create_fast_robot(cls, name):
        """Factory method: creates a Robot with preset speed"""
        # cls = the CLASS itself (like self but for the class)
        return cls(name, speed=2.0)   # cls(name, 2.0) = Robot(name, 2.0)
    # Called as: Robot.create_fast_robot("Speedy")

    # ── STATIC METHOD — belongs to class but uses neither self nor cls ─
    @staticmethod
    def speed_to_kmh(speed_ms):
        """Utility: converts m/s to km/h — doesn't need instance or class"""
        return speed_ms * 3.6
    # Called as: Robot.speed_to_kmh(0.5) or robot.speed_to_kmh(0.5)

    # ── PROPERTY — access a method like an attribute ───────────────
    @property
    def speed_kmh(self):
        """Computed attribute — no () needed when reading"""
        return self.speed * 3.6
    # Read as: robot.speed_kmh  (no parentheses!)

    @speed_kmh.setter
    def speed_kmh(self, value_kmh):
        """Setter for the property"""
        self.speed = value_kmh / 3.6
    # Set as: robot.speed_kmh = 10.0  (no parentheses!)
```

> - `@classmethod` — a **decorator** that marks a class method. First parameter is `cls` (the class itself), not `self`. Used for **factory methods** (alternative constructors) and methods that modify class state.
> - `@staticmethod` — a decorator for utility functions that logically belong to the class but don't need access to instance or class data. No automatic first parameter.
> - `@property` — turns a method into an attribute-like accessor. Read without `()`. Lets you add validation/computation when getting/setting values while keeping the syntax clean.
> - **decorator** (`@something`) — a function that **wraps** another function to modify its behaviour. Written on the line above the function definition.
> - **factory method** — a class method that creates and returns instances with specific configurations. Alternative to having many constructor parameters.

---

```cpp
// ── C++ ───────────────────────────────────────────────────────────
class Robot {
public:
    // INSTANCE METHOD
    void move(double distance) {
        x_ += distance;
    }

    // CONST INSTANCE METHOD — promises not to modify the object
    double getX() const { return x_; }
    // The 'const' after the () makes this a const method
    // Required to call on const objects: const Robot r; r.getX(); ✅

    // STATIC METHOD
    static double speed_to_kmh(double speed_ms) {
        return speed_ms * 3.6;
    }
    // Called as: Robot::speed_to_kmh(0.5)

    // VIRTUAL METHOD — can be overridden by subclasses
    virtual void describe() {
        std::cout << "I am a Robot named " << name_ << "\n";
    }
    // 'virtual' allows polymorphism — see section 9

    // PURE VIRTUAL — must be overridden (abstract method)
    virtual void perform_task() = 0;
    // = 0 makes this method "pure virtual" — no implementation here
    // Any class with a pure virtual method is ABSTRACT

private:
    std::string name_;
    double speed_, x_ = 0.0;
};
```

> - `const` after `()` — a **const member function**: promises not to modify any member variables. Required when calling methods on `const` objects. Put it on all getters.
> - `virtual` — enables **runtime polymorphism**. Without `virtual`, the method called is determined at **compile time** (static dispatch). With `virtual`, it's determined at **runtime** (dynamic dispatch).
> - `= 0` — makes a method **pure virtual** (abstract). The class becomes **abstract** and cannot be instantiated directly.
> - **static dispatch** — the compiler decides which function to call at compile time. Fast but inflexible.
> - **dynamic dispatch** — the program decides which function to call at runtime, based on the actual object type. Slightly slower (vtable lookup) but enables polymorphism.
> - **vtable** (**v**irtual method **table**) — a hidden array of function pointers that C++ uses for dynamic dispatch. Each class with virtual methods has one.

---

```java
// ── JAVA ──────────────────────────────────────────────────────────
public class Robot {

    // INSTANCE METHOD
    public void move(double distance) {
        this.x += distance;
    }

    // STATIC METHOD
    public static double speedToKmh(double speedMs) {
        return speedMs * 3.6;
    }
    // Called as: Robot.speedToKmh(0.5)

    // FINAL METHOD — cannot be overridden by subclasses
    public final void shutdown() {
        System.out.println("Shutting down...");
    }

    // In Java ALL methods are virtual by default (unless final or static)
    // No 'virtual' keyword needed
    public void describe() {
        System.out.println("Robot: " + name);
    }

    private String name;
    private double x = 0.0;
}
```

> - **In Java, all non-final, non-static instance methods are virtual by default**. Unlike C++ where you must explicitly write `virtual`. Java assumes you want polymorphism.
> - `final` method — prevents subclasses from overriding it. The opposite of `virtual` in C++.
> - **camelCase** — Java convention for method and variable names (`speedToKmh`, not `speed_to_kmh`). Classes use PascalCase (`Robot`). Constants use `SCREAMING_SNAKE_CASE` (`MAX_SPEED`).

---

# 6. Constructors & Destructors

## Constructor types

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Motor:

    # DEFAULT CONSTRUCTOR (no required arguments)
    def __init__(self):
        self.rpm   = 0
        self.power = 100

    # PARAMETERISED CONSTRUCTOR (with defaults = optional params)
    def __init__(self, rpm=0, power=100, name="Motor"):
        self.rpm   = rpm
        self.power = power
        self.name  = name
    # Python only allows ONE __init__ per class
    # Use default arguments to simulate multiple constructors

    # DESTRUCTOR — called when object is garbage collected
    def __del__(self):
        print(f"{self.name} destroyed")
    # Python's GC calls this automatically
    # (not guaranteed to run immediately — don't rely on it for critical cleanup)

m1 = Motor()               # Motor(rpm=0, power=100, name="Motor")
m2 = Motor(rpm=1000)       # Motor(rpm=1000, power=100, name="Motor")
m3 = Motor(500, 80, "M3") # Motor(rpm=500, power=80, name="M3")
```

> - **default arguments** — Python's way to have "optional" parameters. If you don't pass them, the default value is used. This simulates multiple constructors.
> - `__del__` — the **destructor**. Called by Python's **garbage collector** when the object's reference count drops to 0. Not guaranteed to run at a specific time — use **context managers** (`with` statement) for reliable cleanup.
> - **garbage collector (GC)** — a runtime mechanism that automatically frees memory when objects are no longer referenced. Python, Java use GC. C++ does not — you manage memory manually (or use smart pointers).
> - **reference count** — Python tracks how many variables point to each object. When it reaches 0, the GC frees the memory.

---

```cpp
// ── C++ ───────────────────────────────────────────────────────────
class Motor {
public:

    // DEFAULT CONSTRUCTOR — no parameters
    Motor() : rpm_(0), power_(100), name_("Motor") {
        std::cout << "Default Motor created\n";
    }

    // PARAMETERISED CONSTRUCTOR
    Motor(int rpm, int power, std::string name)
        : rpm_(rpm), power_(power), name_(name) {}

    // COPY CONSTRUCTOR — creates a new object from an existing one
    Motor(const Motor& other)
        : rpm_(other.rpm_), power_(other.power_), name_(other.name_) {
        std::cout << "Motor copied\n";
    }
    // Called when: Motor m2 = m1;  or  Motor m2(m1);

    // MOVE CONSTRUCTOR — transfers ownership (no copy) — C++11
    Motor(Motor&& other) noexcept
        : rpm_(other.rpm_), power_(other.power_), name_(std::move(other.name_)) {
        other.rpm_   = 0;
        other.power_ = 0;
    }
    // Called when: Motor m2 = std::move(m1);
    // Efficient: transfers resources instead of copying

    // DESTRUCTOR — called automatically on scope exit or delete
    ~Motor() {
        std::cout << name_ << " destroyed\n";
        // Free any heap memory allocated by this object here
    }

private:
    int         rpm_;
    int         power_;
    std::string name_;
};

// Usage:
Motor m1;                         // default constructor
Motor m2(1000, 80, "Main");       // parameterised
Motor m3 = m2;                    // copy constructor
Motor m4 = std::move(m2);         // move constructor (m2 now invalid)
```

> - **copy constructor** `(const Motor& other)` — creates a **new** object as an identical copy of an existing one. `const` = won't modify the original. `&` = takes a reference (avoids infinite recursion if it were by value).
> - **move constructor** `(Motor&& other)` — C++11 feature. `&&` = **rvalue reference**. Transfers resources (like heap memory) from a temporary object instead of copying. Much faster for large objects.
> - `noexcept` — tells the compiler this function won't throw exceptions. Allows optimisations. Good practice on move constructors.
> - `std::move(other.name_)` — **casts** the string to an rvalue reference, allowing its internal buffer to be transferred (stolen) rather than copied.
> - **The Rule of Five** (C++11) — if you define any of: destructor, copy constructor, copy assignment, move constructor, move assignment — you should define all five. Modern C++ often uses the **Rule of Zero** instead: let compiler-generated defaults handle everything by using smart pointers.

---

```java
// ── JAVA ──────────────────────────────────────────────────────────
public class Motor {

    private int    rpm;
    private int    power;
    private String name;

    // DEFAULT CONSTRUCTOR
    public Motor() {
        this(0, 100, "Motor");   // calls the parameterised constructor
        // 'this(...)' = constructor chaining — call another constructor
    }

    // PARAMETERISED CONSTRUCTOR
    public Motor(int rpm, int power, String name) {
        this.rpm   = rpm;
        this.power = power;
        this.name  = name;
    }

    // COPY CONSTRUCTOR — not built-in in Java, must write manually
    public Motor(Motor other) {
        this.rpm   = other.rpm;
        this.power = other.power;
        this.name  = other.name;   // String is immutable — safe to share
    }

    // Java has no destructor — GC handles memory
    // Use try-with-resources for cleanup of files/sockets/etc.
}

// Usage:
Motor m1 = new Motor();
Motor m2 = new Motor(1000, 80, "Main");
Motor m3 = new Motor(m2);   // copy
```

> - `this(...)` — **constructor chaining**: one constructor calls another. Must be the **first statement** in the constructor body. Avoids code duplication.
> - **No destructor in Java** — the GC manages memory. For resources that need explicit cleanup (files, network connections, database connections), Java uses the `Closeable` interface and `try-with-resources`.
> - `try-with-resources` — Java 7+. `try (Motor m = new Motor()) { ... }` automatically calls `m.close()` when the block ends.

---

# 7. Access Modifiers — public · private · protected

```
                    Same      Same      Subclass  Other
                    class     package   anywhere  anywhere
──────────────────────────────────────────────────────────
Python (convention):
  no prefix         ✅         ✅         ✅         ✅     public
  _single           ✅         ✅         ✅         ⚠️     protected (convention)
  __double          ✅         ❌         ❌         ❌     private (name mangling)

C++:
  public            ✅         ✅         ✅         ✅
  protected         ✅         ✅         ✅(sub)    ❌
  private           ✅         ❌         ❌         ❌

Java:
  public            ✅         ✅         ✅         ✅
  protected         ✅         ✅         ✅(sub)    ❌
  (package-private) ✅         ✅         ❌         ❌    (no keyword — default)
  private           ✅         ❌         ❌         ❌
```

> - **package-private** (Java) — the default when no modifier is written. Accessible within the same Java **package** (folder). Stricter than `protected`.
> - **package** (Java) — a namespace that groups related classes. Declared at top of file: `package com.mycompany.robots;`. Like a folder for classes.
> - Python's access control is **by convention only** — nothing technically prevents accessing `_private`. The community considers it bad practice.
> - C++'s `private` and `protected` are **enforced by the compiler** — accessing them causes a compile error.
> - **friend** (C++ only) — a class or function declared `friend` can access private members. Like giving a trusted collaborator a key to the private room.

```cpp
// C++ friend example
class BankAccount {
    friend class Auditor;   // Auditor can access private members
private:
    double balance_ = 1000.0;
};

class Auditor {
public:
    void check(BankAccount& acc) {
        std::cout << acc.balance_;  // ✅ allowed because of friend
    }
};
```

---

# 8. Inheritance — Building on Existing Classes

## Single Inheritance

```python
# ── PYTHON ────────────────────────────────────────────────────────

class Animal:                     # PARENT class (also: base, superclass)
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def breathe(self):
        return f"{self.name} breathes"

    def describe(self):
        return f"{self.name}, age {self.age}"

    def speak(self):              # will be overridden
        return "..."


class Dog(Animal):                # CHILD class (subclass) inherits Animal
    def __init__(self, name, age, breed):
        super().__init__(name, age)   # call parent constructor FIRST
        self.breed = breed            # add child-specific attribute

    def speak(self):              # OVERRIDE parent method
        return "Woof!"

    def fetch(self):              # NEW method only in Dog
        return f"{self.name} fetches the ball"

    def describe(self):           # EXTEND parent method
        parent_desc = super().describe()   # call parent version
        return f"{parent_desc}, breed: {self.breed}"


class Cat(Animal):
    def speak(self):
        return "Meow!"


# Usage
dog = Dog("Rex", 3, "Labrador")
cat = Cat("Whiskers", 5)

print(dog.breathe())      # Rex breathes   — inherited from Animal
print(dog.speak())        # Woof!          — overridden in Dog
print(dog.fetch())        # Rex fetches... — only in Dog
print(dog.describe())     # Rex, age 3, breed: Labrador — extended

# Type checking
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — dog IS-A Animal
print(isinstance(cat, Dog))     # False
```

> - `class Dog(Animal)` — `(Animal)` means Dog **inherits** from Animal. Dog gets all of Animal's attributes and methods automatically.
> - `super()` — refers to the **parent class**. `super().__init__(...)` calls the parent's constructor. Always call this first in the child's `__init__` to ensure the parent is properly set up.
> - **override** — redefining a parent method in a child class. The child's version **replaces** the parent's for that object type.
> - **IS-A relationship** — the key test for inheritance. "A Dog IS-A Animal" ✅. Don't use inheritance for "HAS-A": "A Dog HAS-A collar" → use composition instead (a `collar` attribute).
> - **composition over inheritance** — a design principle: prefer giving a class an attribute of another type rather than inheriting from it. More flexible, less coupled.

---

```cpp
// ── C++ ───────────────────────────────────────────────────────────
#include <iostream>
#include <string>

class Animal {
public:
    Animal(std::string name, int age) : name_(name), age_(age) {}

    void breathe() const {
        std::cout << name_ << " breathes\n";
    }

    virtual void speak() const {         // virtual = can be overridden
        std::cout << "...\n";
    }

    virtual ~Animal() {}                 // ALWAYS make destructor virtual
    // If destructor is NOT virtual, deleting via a base pointer
    // won't call the derived destructor → memory leak

protected:
    std::string name_;   // protected: accessible in Dog, Cat, etc.
    int         age_;
};


class Dog : public Animal {              // public inheritance (most common)
    // public  inheritance: public/protected members stay public/protected
    // private inheritance: all become private
public:
    Dog(std::string name, int age, std::string breed)
        : Animal(name, age)              // call parent constructor
        , breed_(breed)
    {}

    void speak() const override {        // override parent method
        std::cout << "Woof!\n";
        // 'override' keyword: compiler checks this actually overrides something
    }

    void fetch() const {
        std::cout << name_ << " fetches!\n";
    }

private:
    std::string breed_;
};


int main() {
    Dog dog("Rex", 3, "Labrador");
    dog.breathe();        // inherited
    dog.speak();          // overridden: Woof!
    dog.fetch();          // Dog-specific

    // Polymorphism via pointer to base class
    Animal* a = new Dog("Buddy", 2, "Poodle");
    a->speak();           // Woof! — dynamic dispatch via vtable
    delete a;             // ~Dog() called BECAUSE ~Animal() is virtual ✅

    return 0;
}
```

> - `public Animal` — **public inheritance**. The most common type. Public/protected members of Animal remain public/protected in Dog.
> - `protected:` members — accessible in `Dog` (child) but not outside. That's why we use `protected` for `name_` and `age_` — children need them.
> - `override` — C++11 keyword. The compiler verifies the method actually overrides a virtual method from the parent. **Always use it.** Catches typos like `speeek()` that would silently create a new method instead of overriding.
> - `virtual ~Animal() {}` — **virtual destructor** — the single most important rule in C++ inheritance. Without it, `delete animal_ptr` where `animal_ptr` points to a `Dog` would only call `~Animal()`, leaking Dog's resources.

---

```java
// ── JAVA ──────────────────────────────────────────────────────────
public class Animal {
    protected String name;
    protected int    age;

    public Animal(String name, int age) {
        this.name = name;
        this.age  = age;
    }

    public void breathe() {
        System.out.println(name + " breathes");
    }

    public void speak() {              // all methods virtual by default
        System.out.println("...");
    }
}


public class Dog extends Animal {      // 'extends' = inherits
    private String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);              // MUST be first line
        this.breed = breed;
    }

    @Override                          // annotation — not a keyword
    public void speak() {
        System.out.println("Woof!");
    }

    public void fetch() {
        System.out.println(name + " fetches!");
    }
}


// Usage:
Dog dog = new Dog("Rex", 3, "Labrador");
dog.breathe();   // inherited
dog.speak();     // Woof!

Animal a = new Dog("Buddy", 2, "Poodle");  // upcast
a.speak();       // Woof! — polymorphism
```

> - `extends` — Java's keyword for inheritance. A class can `extend` only **one** class (single inheritance). But it can `implement` multiple interfaces.
> - `super(...)` — calls the parent constructor. **Must be the first statement** in the child constructor. Java enforces this.
> - **@Override** — annotation. Not required but strongly recommended. Compiler verifies the method overrides a parent method. Missing `@Override` on a misspelled method would silently create a new method — a hard-to-find bug.
> - **Java allows only single inheritance** of classes. This prevents the **diamond problem** (ambiguity when two parents have the same method). Java solves the need for multiple behaviour inheritance via **interfaces**.

## Multiple Inheritance

```python
# ── PYTHON (allows multiple inheritance) ──────────────────────────
class Flyable:
    def fly(self): return "Flying!"

class Swimmable:
    def swim(self): return "Swimming!"

class Duck(Flyable, Swimmable):   # inherits from BOTH
    def quack(self): return "Quack!"

d = Duck()
print(d.fly())    # Flying!
print(d.swim())   # Swimming!
print(d.quack())  # Quack!

# MRO — Method Resolution Order
# Python uses C3 linearisation to decide which parent's method wins
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>)
# Left to right: Duck → Flyable → Swimmable → object
```

> - **MRO** = **M**ethod **R**esolution **O**rder. When multiple parents have the same method, Python uses the **C3 linearisation algorithm** to determine which one gets called. Generally: left-to-right, depth-first, but with consistency constraints.
> - **diamond problem** — when class D inherits from B and C, and both B and C inherit from A: which A's methods does D get? Python's MRO resolves this. C++ also supports multiple inheritance but requires explicit disambiguation. Java avoids it entirely for classes.
> - `object` — in Python 3, every class implicitly inherits from `object`. It provides `__str__`, `__repr__`, `__hash__`, etc. It's the root of the class hierarchy.

---

# 9. Polymorphism — One Interface Many Behaviours

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclass must implement area()")

class Circle(Shape):
    def __init__(self, radius): self.radius = radius
    def area(self): return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self): return self.w * self.h

class Triangle(Shape):
    def __init__(self, b, h): self.b = b; self.h = h
    def area(self): return 0.5 * self.b * self.h

# POLYMORPHISM — same function call, different behaviour
def print_area(shape: Shape):
    print(f"Area: {shape.area():.2f}")   # calls whichever area() is right

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
for s in shapes:
    print_area(s)         # Area: 78.54 / Area: 24.00 / Area: 12.00
    # print_area doesn't know or care which subclass it has
    # It just calls .area() and polymorphism does the rest
```

```cpp
// ── C++ ───────────────────────────────────────────────────────────
#include <vector>
#include <memory>   // for smart pointers

class Shape {
public:
    virtual double area() const = 0;   // pure virtual = abstract method
    virtual ~Shape() {}
};

class Circle : public Shape {
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
private:
    double r_;
};

class Rectangle : public Shape {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
private:
    double w_, h_;
};

// POLYMORPHISM via base class pointer
void print_area(const Shape& s) {
    std::cout << "Area: " << s.area() << "\n";
    // Calls correct area() at RUNTIME via vtable lookup
}

int main() {
    // Use smart pointers — no manual delete needed
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));

    for (const auto& s : shapes) {
        print_area(*s);   // dereference unique_ptr to get Shape&
    }
    // Smart pointers automatically delete shapes when vector is destroyed
}
```

> - `std::unique_ptr<Shape>` — a **unique smart pointer**. Owns the object exclusively. Automatically calls `delete` when it goes out of scope. **No manual `delete` needed.**
> - `std::make_unique<Circle>(5.0)` — creates a `Circle` on the heap and wraps it in a `unique_ptr`. Prefer this over `new Circle(5.0)`.
> - `const auto&` — `auto` deduces the type (here: `unique_ptr<Shape>`). `const` = won't modify. `&` = reference (no copy).
> - `*s` — **dereferences** the smart pointer to get a `Shape&` reference.
> - `std::shared_ptr` — another smart pointer. Multiple pointers can share ownership. Uses reference counting. Slightly slower than `unique_ptr`.

---

# 10. Abstract Classes & Interfaces

## Abstract Classes

```python
# ── PYTHON — using ABC (Abstract Base Class) ──────────────────────
from abc import ABC, abstractmethod

class Vehicle(ABC):              # ABC makes this an abstract class
    """Cannot be instantiated directly"""

    def __init__(self, brand):
        self.brand = brand       # concrete attribute

    @abstractmethod
    def move(self):              # MUST be implemented by subclasses
        pass
    # @abstractmethod marks this as abstract
    # Subclasses that don't implement it become abstract too

    @abstractmethod
    def fuel_type(self) -> str:
        pass

    def describe(self):          # CONCRETE method — has implementation
        return f"{self.brand}: {self.fuel_type()}"


class ElectricCar(Vehicle):
    def move(self):              # must implement abstract method
        return "Driving silently"
    def fuel_type(self): return "Electric"

class Bicycle(Vehicle):
    def move(self):
        return "Pedalling"
    def fuel_type(self): return "Human power"


# v = Vehicle("Test")        # ❌ TypeError: Can't instantiate abstract class
car = ElectricCar("Tesla")   # ✅
print(car.describe())         # Tesla: Electric
```

> - `ABC` — **A**bstract **B**ase **C**lass. Import from `abc` module. Makes the class abstract.
> - `@abstractmethod` — marks a method as abstract: **must** be overridden in concrete subclasses. If a subclass doesn't implement all abstract methods, it becomes abstract too and can't be instantiated.
> - **concrete class** — a class where all abstract methods are implemented. Can be instantiated.
> - **abstract class** — has at least one abstract method. Cannot be instantiated directly. Serves as a **contract** for subclasses.

---

```java
// ── JAVA — INTERFACE ──────────────────────────────────────────────
// An interface is a pure contract — all methods are abstract by default

public interface Driveable {
    // All methods are public abstract by default
    void accelerate(double amount);
    void brake();
    double getSpeed();

    // DEFAULT method — has an implementation (Java 8+)
    default void horn() {
        System.out.println("Beep!");
    }

    // Static method in interface (Java 8+)
    static boolean isStreetLegal(double speed) {
        return speed <= 120.0;
    }

    // Constants in interfaces are always public static final
    double MAX_SPEED = 200.0;    // implicitly: public static final
}

public interface Electric {
    int getBatteryPercent();
    void charge();
}

// A class can IMPLEMENT multiple interfaces (unlike extends — only one)
public class Tesla extends Vehicle implements Driveable, Electric {
    private double speed    = 0;
    private int    battery  = 100;

    // Must implement ALL methods from Driveable and Electric
    @Override public void   accelerate(double a)  { speed += a; }
    @Override public void   brake()               { speed -= 10; }
    @Override public double getSpeed()            { return speed; }
    @Override public int    getBatteryPercent()   { return battery; }
    @Override public void   charge()              { battery = 100; }
}
```

> - **interface** (Java) — a pure contract. No state (no instance fields). Every class that `implements` it **must** provide all its methods. Like a job description.
> - **`implements`** — Java keyword for using an interface. A class can `extends` one class but `implements` many interfaces.
> - **default method** (Java 8+) — an interface method with an implementation. Allows adding new methods to interfaces without breaking existing implementations.
> - `public static final` — all fields in a Java interface are implicitly this. They're **constants** shared by all implementers.
> - **Why interfaces?** — Java's answer to multiple inheritance. You can't inherit from two classes, but you can implement many interfaces.

---

```cpp
// ── C++ — Abstract class acts as interface ────────────────────────
// C++ has no 'interface' keyword — use abstract classes

class IDriveable {                // convention: prefix 'I' for interface-like
public:
    virtual void accelerate(double amount) = 0;
    virtual void brake()                  = 0;
    virtual double getSpeed() const       = 0;
    virtual ~IDriveable() {}
};

class IElectric {
public:
    virtual int  getBatteryPercent() const = 0;
    virtual void charge()                  = 0;
    virtual ~IElectric() {}
};

// Multiple inheritance of abstract classes = interfaces
class Tesla : public IDriveable, public IElectric {
public:
    void accelerate(double a) override { speed_ += a; }
    void brake()              override { speed_ -= 10; }
    double getSpeed() const   override { return speed_; }
    int  getBatteryPercent() const override { return battery_; }
    void charge()              override { battery_ = 100; }

private:
    double speed_   = 0.0;
    int    battery_ = 100;
};
```

---

# 11. Static Members

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Config:
    """A static-only utility class — all class variables and methods"""

    MAX_SPEED    = 2.0       # class constant
    DEFAULT_NAME = "Robot"
    _instance_count = 0      # private class variable

    @classmethod
    def get_count(cls):
        return cls._instance_count

    @staticmethod
    def validate_speed(speed):
        return 0.0 <= speed <= Config.MAX_SPEED
```

```cpp
// ── C++ ───────────────────────────────────────────────────────────
class Config {
public:
    static constexpr double MAX_SPEED    = 2.0;     // compile-time constant
    static constexpr int    MAX_ROBOTS   = 100;
    static const std::string DEFAULT_NAME;           // defined outside

    static bool validate_speed(double s) {
        return s >= 0.0 && s <= MAX_SPEED;
    }

    static int get_robot_count() { return robot_count_; }

private:
    static int robot_count_;   // DECLARED here
};

// DEFINED outside:
const std::string Config::DEFAULT_NAME = "Robot";
int               Config::robot_count_ = 0;

// Usage — no object needed:
Config::validate_speed(1.5);
int max = Config::MAX_ROBOTS;
```

```java
// ── JAVA ──────────────────────────────────────────────────────────
public class Config {
    public  static final double MAX_SPEED    = 2.0;   // constant
    public  static final int    MAX_ROBOTS   = 100;
    private static       int    robotCount   = 0;

    public static boolean validateSpeed(double s) {
        return s >= 0.0 && s <= MAX_SPEED;
    }

    public static int getRobotCount() { return robotCount; }
}

// Usage:
Config.validateSpeed(1.5);
int max = Config.MAX_ROBOTS;
```

> - `static` members belong to the **class**, not to any instance. One copy shared by all.
> - `constexpr` (C++) — evaluated at **compile time**. The fastest kind of constant. Use for numeric constants.
> - `final` (Java) — a variable that cannot be reassigned after initialisation. `static final` = a class-level constant.
> - **Utility class** — a class with only static methods and constants. Never instantiated. Like a namespace with functions. `Math`, `Arrays`, `Collections` in Java are examples.

---

# 12. Special Methods & Operator Overloading

## Python Dunder Methods

```python
class Vector2D:
    """A 2D vector — demonstrates Python's special (dunder) methods"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # ── STRING REPRESENTATION ─────────────────────────────────────
    def __str__(self):
        """Called by print() and str() — human-readable"""
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        """Called in REPL/debug — should be unambiguous, ideally eval-able"""
        return f"Vector2D(x={self.x}, y={self.y})"

    # ── ARITHMETIC OPERATORS ──────────────────────────────────────
    def __add__(self, other):       # self + other
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):       # self - other
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):      # self * scalar
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):     # scalar * self  (reversed)
        return self.__mul__(scalar)

    def __neg__(self):              # -self (unary minus)
        return Vector2D(-self.x, -self.y)

    def __abs__(self):              # abs(self)
        import math
        return math.sqrt(self.x**2 + self.y**2)

    # ── COMPARISON OPERATORS ──────────────────────────────────────
    def __eq__(self, other):        # self == other
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):        # self < other (for sorting)
        return abs(self) < abs(other)

    # ── CONTAINER BEHAVIOUR ───────────────────────────────────────
    def __len__(self):              # len(self)
        return 2                   # a 2D vector has 2 components

    def __getitem__(self, index):   # self[index]
        if index == 0: return self.x
        if index == 1: return self.y
        raise IndexError("Vector2D index out of range")

    def __iter__(self):             # for item in self:
        yield self.x
        yield self.y

    # ── CONTEXT MANAGER ───────────────────────────────────────────
    def __enter__(self):            # with Vector2D(...) as v:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        return False                # don't suppress exceptions

    # ── CALLABLE ─────────────────────────────────────────────────
    def __call__(self, scale):      # obj(args) — use object as function
        return self * scale


# Usage:
v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)

print(v1)              # Vector(1, 2)       — __str__
print(repr(v1))        # Vector2D(x=1, y=2) — __repr__
print(v1 + v2)         # Vector(4, 6)       — __add__
print(v1 * 3)          # Vector(3, 6)       — __mul__
print(3 * v1)          # Vector(3, 6)       — __rmul__
print(abs(v1))         # 2.236...           — __abs__
print(v1 == v2)        # False              — __eq__
print(v1[0])           # 1                  — __getitem__
print(len(v1))         # 2                  — __len__
print(list(v1))        # [1, 2]             — __iter__
print(v1(5))           # Vector(5, 10)      — __call__

vectors = [v2, v1, Vector2D(0,0)]
vectors.sort()         # uses __lt__ for comparison
```

> - **dunder** = **d**ouble **under**score. Methods like `__add__`, `__str__` are called automatically by Python operators and built-in functions. You define them to make your class work with Python's syntax naturally.
> - `__str__` vs `__repr__` — `str()` for humans (readable). `repr()` for developers (unambiguous, ideally valid Python that recreates the object).
> - `__rmul__` — the **reflected** version. When Python evaluates `3 * v1`, it first tries `(3).__mul__(v1)`. If that returns `NotImplemented`, it tries `v1.__rmul__(3)`.
> - `__call__` — makes an object **callable** (can be called like a function: `obj(args)`). Used in decorators, functors, and machine learning layers.
> - `yield` — makes `__iter__` a **generator**. Each `yield` pauses execution and returns a value to the `for` loop. Resumes from where it left off on the next iteration.
> - **context manager** (`__enter__`/`__exit__`) — enables the `with` statement. `__enter__` runs on entry, `__exit__` runs on exit (even if an exception occurred). Used for resource management.

---

## C++ Operator Overloading

```cpp
#include <cmath>
#include <iostream>

class Vector2D {
public:
    double x, y;

    Vector2D(double x, double y) : x(x), y(y) {}

    // ── ARITHMETIC OPERATORS (member functions) ───────────────────
    Vector2D operator+(const Vector2D& other) const {
        return {x + other.x, y + other.y};
        // Return by value — creates a new Vector2D
    }

    Vector2D operator-(const Vector2D& other) const {
        return {x - other.x, y - other.y};
    }

    Vector2D operator*(double scalar) const {
        return {x * scalar, y * scalar};
    }

    Vector2D operator-() const {          // unary minus: -v
        return {-x, -y};
    }

    // ── COMPOUND ASSIGNMENT ───────────────────────────────────────
    Vector2D& operator+=(const Vector2D& other) {
        x += other.x;
        y += other.y;
        return *this;   // return reference to self for chaining: v1 += v2 += v3
    }

    // ── COMPARISON ────────────────────────────────────────────────
    bool operator==(const Vector2D& other) const {
        return x == other.x && y == other.y;
    }

    bool operator<(const Vector2D& other) const {
        return magnitude() < other.magnitude();
    }

    // ── INDEX OPERATOR ────────────────────────────────────────────
    double& operator[](int i) {
        if (i == 0) return x;
        if (i == 1) return y;
        throw std::out_of_range("Vector2D: index out of range");
    }

    double magnitude() const {
        return std::sqrt(x*x + y*y);
    }
};

// ── OPERATORS that need left operand to be non-class ─────────────
// (must be FREE FUNCTIONS, not member functions)

// scalar * vector  (3.0 * v  not  v * 3.0)
Vector2D operator*(double scalar, const Vector2D& v) {
    return {scalar * v.x, scalar * v.y};
}

// << for output streams (cout)
std::ostream& operator<<(std::ostream& os, const Vector2D& v) {
    return os << "Vector(" << v.x << ", " << v.y << ")";
    // return os for chaining: cout << v1 << " and " << v2
}

// Usage:
Vector2D v1(1, 2), v2(3, 4);
std::cout << v1 + v2  << "\n";   // Vector(4, 6)
std::cout << 3.0 * v1 << "\n";   // Vector(3, 6)
std::cout << (v1 == v2)  << "\n"; // 0 (false)
std::cout << v1[0]       << "\n"; // 1
v1 += v2;
std::cout << v1 << "\n";          // Vector(4, 6)
```

> - `operator+` — defines what `v1 + v2` does. The operator is a **function named `operator+`**. You call it normally with the operator syntax.
> - `const Vector2D& other` — takes the right operand by **const reference**: no copy, no modification.
> - `return *this` — returns a reference to **this** object. Needed for compound assignment (`+=`) to allow chaining: `a += b += c`.
> - **free function** vs **member function** operators — when the left operand isn't your class (like `3.0 * v`), you can't make it a member. Write a free function instead.
> - `std::ostream& operator<<` — the **output stream operator**. Returns `ostream&` for chaining (`cout << v1 << v2`).

---

# 13. Templates & Generics

## C++ Templates

```cpp
// ── FUNCTION TEMPLATE ─────────────────────────────────────────────
template <typename T>
// 'template' keyword. T is a placeholder type (generic type parameter)
// T can be any type: int, double, std::string, Robot, etc.

T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// Usage — compiler generates a specific version for each type:
maximum(3, 5);           // maximum<int>(3, 5)
maximum(3.14, 2.71);    // maximum<double>(3.14, 2.71)
maximum('a', 'z');       // maximum<char>('a', 'z')


// ── CLASS TEMPLATE ────────────────────────────────────────────────
template <typename T, int Capacity = 10>
// T = type of elements. Capacity = a non-type template parameter with default

class Stack {
public:
    void push(const T& item) {
        if (size_ < Capacity) data_[size_++] = item;
    }

    T pop() {
        if (size_ == 0) throw std::underflow_error("Stack is empty");
        return data_[--size_];
    }

    T& top()        { return data_[size_ - 1]; }
    bool empty()    const { return size_ == 0; }
    int  size()     const { return size_; }

private:
    T   data_[Capacity];  // array of type T with compile-time size
    int size_ = 0;
};

// Usage:
Stack<int>          int_stack;          // Stack of ints, capacity 10
Stack<std::string>  str_stack;          // Stack of strings
Stack<double, 50>   big_stack;          // Stack of doubles, capacity 50

int_stack.push(1);
int_stack.push(2);
std::cout << int_stack.pop() << "\n";   // 2
```

> - `template <typename T>` — declares a **template**. The compiler generates a **concrete version** for every type you use (`Stack<int>`, `Stack<double>`, etc.). This is called **template instantiation**.
> - `typename T` — `T` is a placeholder for any type. You can also write `class T` (same meaning in this context). `T` is just a convention — you can name it anything.
> - **Non-type template parameter** `int Capacity = 10` — a compile-time integer (not a type). Allows things like fixed-size arrays in templates.
> - **Template instantiation** — the compiler generates a separate function/class for each unique combination of template arguments. `Stack<int>` and `Stack<double>` are completely separate classes.
> - **compile time** — during compilation, before the program runs. Template parameters must be known at compile time.

## Java Generics

```java
// ── GENERIC CLASS ────────────────────────────────────────────────
public class Stack<T> {
// <T> = type parameter. T is the placeholder for the actual type.

    private Object[] data;     // Java generics use type erasure
    private int      size = 0;
    private int      capacity;

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
        return (T) data[--size];   // cast required because of type erasure
    }

    public boolean isEmpty() { return size == 0; }
    public int     getSize() { return size; }
}


// ── BOUNDED TYPE PARAMETERS ───────────────────────────────────────
// Restrict T to only types that are Comparable
public class SortedList<T extends Comparable<T>> {
// T extends Comparable<T> = T must implement the Comparable interface
// This lets us call .compareTo() on T objects

    public T findMin(List<T> list) {
        T min = list.get(0);
        for (T item : list) {
            if (item.compareTo(min) < 0) min = item;
        }
        return min;
    }
}


// Usage:
Stack<Integer> intStack = new Stack<>(10);
Stack<String>  strStack = new Stack<>(20);

intStack.push(42);
System.out.println(intStack.pop());    // 42
```

> - **type erasure** — Java generics are implemented via **type erasure**: at compile time, `Stack<Integer>` is verified, but at runtime, the JVM sees `Stack<Object>`. Type info is erased. This is why the internal array must be `Object[]`.
> - `@SuppressWarnings("unchecked")` — suppresses the compiler warning about unchecked casts. Needed when type erasure forces you to cast from `Object` to `T`.
> - `T extends Comparable<T>` — a **bounded type parameter**: restricts `T` to types that implement `Comparable<T>`. `Integer`, `String`, `Double` all implement `Comparable`.
> - `Comparable<T>` — a Java interface with one method: `int compareTo(T other)`. Returns negative (less than), 0 (equal), positive (greater than).
> - **Difference from C++ templates** — C++ generates actual separate code per type (templates). Java uses one class with `Object` and casts (type erasure). Java generics catch errors at compile time but have no runtime overhead difference.

## Python Generics (Type Hints)

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')    # declare a type variable

class Stack(Generic[T]):    # Generic[T] = parameterised by T
    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self) -> T:
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0


# Usage with type hints (mypy will check types):
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())   # 2
```

> - **TypeVar** — defines a type variable for use in type hints. `T = TypeVar('T')`.
> - **Type hints in Python are optional** and not enforced at runtime. They're for **static analysis tools** like `mypy` or IDE autocompletion. Python remains dynamically typed.
> - `Generic[T]` — makes the class parameterisable with a type. Purely for type checking — no runtime difference.
> - `List[T]` — a list whose elements are of type `T`. From `typing` module. In Python 3.9+, you can write `list[T]` directly.

---

# 14. Memory Management

## The 3 Approaches

```
Language    Memory management     You manage?   Crashes possible?
──────────────────────────────────────────────────────────────────
C           Manual (malloc/free)  ✅ Yes        ✅ Yes (leaks, dangling)
C++         Manual + Smart ptrs   Mostly no     ⚠️ If using raw pointers
Python      Garbage Collector      ❌ No         ❌ No (GC handles it)
Java        Garbage Collector      ❌ No         ❌ No (GC handles it)
```

## C++ Smart Pointers

```cpp
#include <memory>

// ── unique_ptr — single exclusive owner ───────────────────────────
{
    std::unique_ptr<Robot> r = std::make_unique<Robot>("R2D2", 0.5);
    r->move(1.0);
    // r automatically deleted when this scope ends
}
// r is destroyed here — ~Robot() called automatically

// Transfer ownership (can't copy a unique_ptr):
auto r2 = std::move(r);    // r is now null, r2 owns the object


// ── shared_ptr — shared ownership ────────────────────────────────
{
    auto r1 = std::make_shared<Robot>("C-3PO", 0.3);
    auto r2 = r1;     // BOTH r1 and r2 own the Robot — reference count = 2
    // reference count = how many shared_ptrs point to the object

    r1.reset();       // r1 releases — count drops to 1
    // r2 still alive — Robot not destroyed yet
}
// r2 goes out of scope — count = 0 — Robot destroyed


// ── weak_ptr — observe without owning ────────────────────────────
std::weak_ptr<Robot> w;
{
    auto r = std::make_shared<Robot>("BB-8", 0.7);
    w = r;            // w observes r — does NOT increment ref count
    // Use .lock() to temporarily own:
    if (auto locked = w.lock()) {
        locked->move(1.0);   // safe — locked is a shared_ptr
    }
}
// r destroyed — w is now expired (w.lock() returns null)
```

> - `unique_ptr` — **exclusive ownership**. Only one `unique_ptr` can point to an object at a time. Cannot be copied, only moved. Use for most heap objects. Zero overhead vs raw pointer.
> - `shared_ptr` — **shared ownership**. Multiple `shared_ptr`s can point to the same object. Destroyed when the last one goes away. Uses **reference counting** — slight overhead.
> - `weak_ptr` — **non-owning observer**. Doesn't keep the object alive. Must `lock()` to access (returns `shared_ptr` if still alive, null if destroyed). Used to break **circular references** (where two shared_ptrs point to each other — they'd never be freed).
> - **circular reference** — A → B → A. Both have reference count ≥ 1, so GC never frees them. `weak_ptr` breaks the cycle.
> - `.reset()` — releases ownership. The pointer becomes null.
> - **RAII** = **R**esource **A**cquisition **I**s **I**nitialisation. The C++ idiom: tie resource lifetime to object lifetime. When the smart pointer is created → resource acquired. When destroyed → resource released. Smart pointers implement RAII for heap memory.

---

# 15. OOP in C — Simulating with Structs

C has no native OOP. But you can **simulate** it with `struct` and function pointers.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ── STEP 1: Define the "class" as a struct ────────────────────────
typedef struct Robot Robot;
// Forward declaration: Robot is a struct (needed for function pointers below)
// typedef: creates an alias so you can write 'Robot' instead of 'struct Robot'

struct Robot {
    // ── DATA (attributes) ─────────────────────────────────────────
    char   name[50];
    double speed;
    double x;

    // ── FUNCTION POINTERS (methods) ───────────────────────────────
    void   (*move)(Robot* self, double distance);
    void   (*stop)(Robot* self);
    double (*get_x)(const Robot* self);
    // A function pointer: void (*move)(Robot*) = pointer to a function
    // that takes Robot* and returns void
};


// ── STEP 2: Define the functions (implementations) ────────────────
void robot_move(Robot* self, double distance) {
    // self = the object — manual equivalent of Python's 'self' / C++'s 'this'
    self->x += distance;
    // -> accesses struct members through a pointer
    printf("%s moved to x=%.2f\n", self->name, self->x);
}

void robot_stop(Robot* self) {
    self->speed = 0.0;
    printf("%s stopped\n", self->name);
}

double robot_get_x(const Robot* self) {
    return self->x;
}


// ── STEP 3: "Constructor" — initialise the struct ─────────────────
Robot* Robot_new(const char* name, double speed) {
    Robot* r = (Robot*)malloc(sizeof(Robot));
    // malloc: allocate sizeof(Robot) bytes on the heap
    // (Robot*) : cast the void* returned by malloc to Robot*

    if (!r) return NULL;   // check allocation succeeded

    strncpy(r->name, name, 49);
    r->name[49] = '\0';    // ensure null termination (safety)
    r->speed = speed;
    r->x     = 0.0;

    // Assign function pointers (bind methods to object)
    r->move  = robot_move;
    r->stop  = robot_stop;
    r->get_x = robot_get_x;

    return r;
}


// ── STEP 4: "Destructor" — free memory ────────────────────────────
void Robot_delete(Robot* r) {
    if (r) free(r);   // free the heap memory
    // free: releases malloc'd memory back to the OS
}


// ── STEP 5: Simulate inheritance with struct embedding ───────────
typedef struct {
    Robot base;        // FIRST MEMBER = the "parent" struct
    // A pointer to DroneRobot can be safely cast to Robot*
    // because base is the first member

    double altitude;   // drone-specific attribute

    void (*fly)(struct DroneRobot* self, double height);
} DroneRobot;

void drone_fly(DroneRobot* self, double height) {
    self->altitude = height;
    printf("%s flying at %.1fm\n", self->base.name, height);
}

DroneRobot* DroneRobot_new(const char* name, double speed) {
    DroneRobot* d = (DroneRobot*)malloc(sizeof(DroneRobot));
    // Initialise the Robot base first:
    Robot_new_inplace((Robot*)d, name, speed);   // hypothetical helper
    d->altitude = 0.0;
    d->fly      = drone_fly;
    return d;
}


// ── USAGE ─────────────────────────────────────────────────────────
int main() {
    Robot* r = Robot_new("R2D2", 0.5);

    r->move(r, 1.5);     // call via function pointer — must pass r manually
    r->stop(r);
    printf("x = %.2f\n", r->get_x(r));

    Robot_delete(r);     // must manually free!

    return 0;
}
```

> - `struct` — C's way to group data. No methods, no access control, no inheritance natively.
> - `typedef struct Robot Robot` — creates an alias so you write `Robot` instead of `struct Robot`. C (unlike C++) requires `struct` keyword otherwise.
> - **function pointer** `void (*move)(Robot*)` — a variable that stores the address of a function. This is C's equivalent of a method — you store the function's address and call it through the pointer. The syntax is awkward but powerful.
> - `->` — accesses a struct member **through a pointer**. `r->name` = `(*r).name`. Used because `r` is a pointer (`Robot*`), not a value.
> - `malloc(size)` — **m**emory **alloc**ation. Allocates `size` bytes on the heap. Returns `void*` (untyped pointer). Must be cast to the correct type. Returns `NULL` if allocation fails.
> - `free(ptr)` — releases heap memory. **Must** call this for every `malloc`. Forgetting = **memory leak**.
> - **null termination** — C strings (char arrays) end with `'\0'` (the null character). Functions like `printf` scan for `'\0'` to know where the string ends. `strncpy` with a buffer requires you to manually set the last byte to `'\0'`.
> - **struct embedding** for inheritance — placing the parent struct as the **first member** of the child struct. A pointer to the child can be safely cast to a pointer to the parent, because their memory starts at the same address.

---

# 16. Design Patterns

Common reusable OOP solutions to recurring problems.

## Singleton — Only One Instance

```python
# ── PYTHON ────────────────────────────────────────────────────────
class RobotConfig:
    """Only one configuration object should exist"""

    _instance = None    # class variable: the single instance

    def __new__(cls):
        # __new__ creates the object (called BEFORE __init__)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.speed    = 0.5
            cls._instance.debug    = False
        return cls._instance   # always returns the same object

c1 = RobotConfig()
c2 = RobotConfig()
print(c1 is c2)   # True — same object!
```

```cpp
// ── C++ ───────────────────────────────────────────────────────────
class RobotConfig {
public:
    static RobotConfig& getInstance() {
        static RobotConfig instance;   // created once, on first call
        return instance;               // local static = thread-safe in C++11
    }

    double speed = 0.5;
    bool   debug = false;

private:
    RobotConfig() {}                              // private constructor
    RobotConfig(const RobotConfig&) = delete;    // no copy
    void operator=(const RobotConfig&) = delete; // no assignment
};

auto& cfg = RobotConfig::getInstance();
cfg.speed = 1.0;
```

> - **Singleton** — ensures only **one instance** of a class exists. Used for: configuration managers, logging systems, hardware interfaces.
> - `__new__` (Python) — called **before** `__init__`. Creates and returns the raw object. Overriding it lets you control instance creation.
> - `static local variable` (C++) — a local variable that persists across function calls and is initialised only once. In C++11+, initialisation is guaranteed to be **thread-safe**.
> - `= delete` — C++11 way to **disable** a constructor or operator. Prevents copy and assignment of the singleton.

## Observer — Event Notification

```python
# ── PYTHON ────────────────────────────────────────────────────────
class EventEmitter:
    """Objects can subscribe to events and be notified when they fire"""

    def __init__(self):
        self._listeners = {}   # dict: event_name → list of callbacks

    def on(self, event, callback):
        """Register a listener for an event"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event, *args, **kwargs):
        """Fire an event — call all registered listeners"""
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class Robot(EventEmitter):
    def __init__(self, name):
        super().__init__()
        self.name  = name
        self.speed = 0.0

    def set_speed(self, speed):
        old = self.speed
        self.speed = speed
        self.emit('speed_changed', old_speed=old, new_speed=speed)


# Usage:
robot = Robot("R2D2")

# Subscribe to events
robot.on('speed_changed',
         lambda old, new: print(f"Speed: {old} → {new}"))

robot.set_speed(0.5)    # prints: Speed: 0.0 → 0.5
robot.set_speed(1.0)    # prints: Speed: 0.5 → 1.0
```

> - **Observer pattern** — defines a one-to-many relationship: when one object changes state, all its dependents are notified. Also called **event-driven** programming or **pub/sub**.
> - `*args, **kwargs` — pass any positional and keyword arguments through to callbacks. Makes the emitter generic.
> - `lambda` — an anonymous (unnamed) function. `lambda x: x+1` = a function that takes x and returns x+1. Useful for short callbacks.

## Factory — Create Objects Without Knowing Their Exact Type

```python
# ── PYTHON ────────────────────────────────────────────────────────
class Robot: pass
class DroneRobot(Robot): pass
class WheelRobot(Robot): pass
class ArmRobot(Robot):   pass

class RobotFactory:
    @staticmethod
    def create(robot_type: str) -> Robot:
        registry = {
            'drone':  DroneRobot,
            'wheel':  WheelRobot,
            'arm':    ArmRobot,
        }
        if robot_type not in registry:
            raise ValueError(f"Unknown robot type: {robot_type}")
        return registry[robot_type]()   # instantiate the correct class

r = RobotFactory.create('drone')   # returns DroneRobot()
# Caller doesn't need to know the class name
```

> - **Factory pattern** — a method/class that creates objects without the caller knowing the exact class. Decouples the code that uses objects from the code that creates them.
> - **registry** (dict of name→class) — a common Python pattern for factories. Classes are first-class objects in Python — they can be stored in dicts and called.

---

# 17. Full Robot Class Example — All 4 Languages

## 🐍 Python

```python
from abc import ABC, abstractmethod
import math

class Robot(ABC):
    """Abstract base robot"""

    _total = 0

    def __init__(self, name: str, speed: float, x: float = 0.0, y: float = 0.0):
        self._name  = name
        self._speed = speed
        self._x     = x
        self._y     = y
        Robot._total += 1

    @abstractmethod
    def perform_task(self) -> str: pass

    def move_to(self, tx: float, ty: float):
        dist = math.sqrt((tx - self._x)**2 + (ty - self._y)**2)
        self._x, self._y = tx, ty
        return dist

    @property
    def position(self):
        return (self._x, self._y)

    @staticmethod
    def get_total(): return Robot._total

    def __str__(self):
        return f"{self.__class__.__name__}({self._name}) at {self.position}"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name!r}, speed={self._speed})"


class GroundRobot(Robot):
    def __init__(self, name, speed, wheel_radius=0.05):
        super().__init__(name, speed)
        self._wheel_radius = wheel_radius

    def perform_task(self):
        return f"{self._name} rolling on ground"

    def calculate_rpm(self):
        circumference = 2 * math.pi * self._wheel_radius
        return (self._speed / circumference) * 60


class DroneRobot(Robot):
    def __init__(self, name, speed, max_altitude=50.0):
        super().__init__(name, speed)
        self._altitude     = 0.0
        self._max_altitude = max_altitude

    def perform_task(self):
        return f"{self._name} flying at {self._altitude}m"

    def fly_to(self, altitude: float):
        self._altitude = min(altitude, self._max_altitude)


# Usage
ground = GroundRobot("Rover", speed=0.5)
drone  = DroneRobot("Eagle", speed=2.0, max_altitude=100.0)

print(ground.perform_task())
print(drone.perform_task())
print(Robot.get_total())      # 2

robots = [ground, drone]
for r in robots:
    r.move_to(1.0, 2.0)
    print(r)
```

---

## ⚙️ C++

```cpp
#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <memory>

class Robot {
public:
    static int total;

    Robot(std::string name, double speed, double x=0, double y=0)
        : name_(name), speed_(speed), x_(x), y_(y) { ++total; }

    virtual ~Robot() { --total; }

    virtual std::string perform_task() const = 0;

    double move_to(double tx, double ty) {
        double dist = std::hypot(tx - x_, ty - y_);
        x_ = tx; y_ = ty;
        return dist;
    }

    std::string get_name()  const { return name_; }
    double      get_speed() const { return speed_; }
    double      get_x()     const { return x_; }
    double      get_y()     const { return y_; }

    static int get_total() { return total; }

    virtual void print() const {
        std::cout << name_ << " at (" << x_ << ", " << y_ << ")\n";
    }

protected:
    std::string name_;
    double speed_, x_, y_;
};
int Robot::total = 0;


class GroundRobot : public Robot {
public:
    GroundRobot(std::string name, double speed, double wheel_r=0.05)
        : Robot(name, speed), wheel_radius_(wheel_r) {}

    std::string perform_task() const override {
        return name_ + " rolling on ground";
    }

    double calculate_rpm() const {
        double circ = 2 * M_PI * wheel_radius_;
        return (speed_ / circ) * 60.0;
    }

private:
    double wheel_radius_;
};


class DroneRobot : public Robot {
public:
    DroneRobot(std::string name, double speed, double max_alt=50.0)
        : Robot(name, speed), altitude_(0), max_altitude_(max_alt) {}

    std::string perform_task() const override {
        return name_ + " flying at " + std::to_string(altitude_) + "m";
    }

    void fly_to(double alt) {
        altitude_ = std::min(alt, max_altitude_);
    }

private:
    double altitude_, max_altitude_;
};


int main() {
    std::vector<std::unique_ptr<Robot>> robots;
    robots.push_back(std::make_unique<GroundRobot>("Rover", 0.5));
    robots.push_back(std::make_unique<DroneRobot>("Eagle", 2.0, 100.0));

    for (auto& r : robots) {
        std::cout << r->perform_task() << "\n";
        r->move_to(1.0, 2.0);
        r->print();
    }

    std::cout << "Total robots: " << Robot::get_total() << "\n";   // 2
    return 0;
}
```

---

## ☕ Java

```java
import java.util.*;

public abstract class Robot {
    private static int total = 0;

    protected String name;
    protected double speed;
    protected double x, y;

    public Robot(String name, double speed) {
        this.name = name; this.speed = speed;
        this.x = 0; this.y = 0;
        total++;
    }

    public abstract String performTask();

    public double moveTo(double tx, double ty) {
        double dist = Math.hypot(tx - x, ty - y);
        this.x = tx; this.y = ty;
        return dist;
    }

    public String getName()  { return name; }
    public static int getTotal() { return total; }

    @Override
    public String toString() {
        return getClass().getSimpleName() + "(" + name + ") at (" + x + ", " + y + ")";
    }
}

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

# 18. Language Comparison Cheat Sheet

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
| `self` / `this` | `self` (explicit) | `this` (implicit) | `this` (implicit) | `self` pointer (manual) |
| Call parent | `super().__init__()` | `: Y(args)` | `super()` | `Y_init((Y*)self)` |
| Public | (default) | `public:` | `public` | (default in struct) |
| Private | `__prefix` | `private:` | `private` | N/A (convention) |
| Protected | `_prefix` | `protected:` | `protected` | N/A |
| Override | `def method(self)` | `override` keyword | `@Override` | replace function ptr |
| Virtual method | all methods | `virtual` keyword | all methods | function pointer |
| Static member | class variable | `static` | `static` | global variable |
| Static method | `@staticmethod` | `static` method | `static` method | free function |
| Operator overload | `__add__` etc. | `operator+` etc. | ❌ not supported | ❌ |
| Multiple inherit | ✅ | ✅ (careful) | ❌ classes only | ❌ |
| Templates/Generics | `TypeVar`/hints | `template<T>` | `<T>` generics | macros / void* |
| Memory | GC | manual / smart ptr | GC | `malloc`/`free` |

## Abbreviation Glossary

| Abbreviation | Full form |
|---|---|
| OOP | Object-Oriented Programming |
| GC | Garbage Collector |
| ABC | Abstract Base Class |
| API | Application Programming Interface |
| MRO | Method Resolution Order |
| RAII | Resource Acquisition Is Initialisation |
| REPL | Read-Eval-Print Loop |
| vtable | Virtual method table |
| DOF | Degrees Of Freedom (joint context) |
| LTS | Long Term Support |
| JVM | Java Virtual Machine |
| GC | Garbage Collector |
| PascalCase | NamingConvention (each word capitalised) |
| camelCase | namingConvention (first word lowercase) |
| snake_case | naming_convention (underscores) |
| SCREAMING_SNAKE | CONSTANT_NAMING_CONVENTION |
