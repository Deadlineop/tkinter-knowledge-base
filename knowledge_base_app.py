"""
Knowledge Base: Facts and Predicates
A Tkinter GUI that stores facts such as Professor(Lucy) or Likes(John, Susie)
and answers queries about them, including wildcard queries like Parent(John, ?).
"""
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# ---------------------------------------------------------------------------
# Data: known predicates -> (number of arguments, meaning template)
# ---------------------------------------------------------------------------
PREDICATES = {
    "Professor": (1, "{0} is a professor"),
    "Male":      (1, "{0} is male"),
    "Student":   (1, "{0} is a student"),
    "Likes":     (2, "{0} likes {1}"),
    "Parent":    (2, "{0} is {1}'s parent"),
    "Between":   (3, "A relationship among {0}, {1} and {2}"),
}

# Facts are stored as tuples: (predicate, arg1, arg2, ...)
facts = {
    ("Professor", "Lucy"), ("Professor", "Danny"),
    ("Male", "Adam"),
    ("Student", "Ravi"),
    ("Likes", "John", "Susie"),
    ("Parent", "John", "Adam"), ("Parent", "Mary", "Susan"),
    ("Between", "A", "B", "C"),
}


def fact_to_text(fact):
    """('Likes', 'John', 'Susie') -> 'Likes(John, Susie)'"""
    return "{}({})".format(fact[0], ", ".join(fact[1:]))


def meaning(fact):
    arity, template = PREDICATES.get(fact[0], (len(fact) - 1, "user-defined predicate"))
    return template.format(*fact[1:])


# Small helper functions, same idea as the set-based examples
def is_professor(person):
    return ("Professor", person) in facts


def is_parent(parent, child):
    return ("Parent", parent, child) in facts


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
a = Tk()
a.title("Knowledge Base - Facts and Predicates")
a.geometry("940x720")
a.configure(bg="#f4f6fb")
a.columnconfigure(0, weight=1)
a.columnconfigure(1, weight=1)
a.rowconfigure(2, weight=1)

ignore_case = BooleanVar(value=True)
status = StringVar(value="Ready")

title = Label(a, text="Knowledge Base: Facts and Predicates",
              font=("Arial", 20, "bold"), fg="#1a4fa0", bg="#f4f6fb")
title.grid(row=0, column=0, columnspan=2, pady=(12, 0))
Label(a, text="Add facts like Professor(Lucy), then ask questions like Parent(John, ?)",
      font=("Arial", 11), fg="#555", bg="#f4f6fb").grid(row=1, column=0, columnspan=2, pady=(0, 8))


def make_arg_entries(parent, row):
    """Three argument boxes; only as many as the predicate needs are enabled."""
    entries = []
    for i in range(3):
        Label(parent, text="Arg {}".format(i + 1), bg="white").grid(row=row, column=i, sticky=W, padx=6)
        e = Entry(parent, width=13, font=("Arial", 11))
        e.grid(row=row + 1, column=i, padx=6, pady=(0, 6), sticky=EW)
        entries.append(e)
    return entries


def set_arity(entries, arity):
    for i, e in enumerate(entries):
        if i < arity:
            e.config(state=NORMAL, bg="white")
        else:
            e.delete(0, END)
            e.config(state=DISABLED, disabledbackground="#e6e6e6")


def read_fact(pred_box, arity_box, entries, allow_wildcard=False):
    """Collect predicate + arguments from the widgets, with validation."""
    pred = pred_box.get().strip()
    if not pred:
        raise ValueError("Choose or type a predicate name.")
    pred = pred[0].upper() + pred[1:]
    arity = int(arity_box.get())
    args = [entries[i].get().strip() for i in range(arity)]
    if any(x == "" for x in args):
        raise ValueError("Fill all {} argument(s) for {}.".format(arity, pred))
    if not allow_wildcard and "?" in args:
        raise ValueError("'?' is only allowed in queries.")
    return tuple([pred] + args)


# ---------------------------------------------------------------------------
# Left: Add a fact
# ---------------------------------------------------------------------------
add_frame = LabelFrame(a, text=" Add a Fact ", font=("Arial", 12, "bold"), bg="white", padx=8, pady=8)
add_frame.grid(row=2, column=0, sticky=NSEW, padx=(14, 7), pady=4)

Label(add_frame, text="Predicate", bg="white").grid(row=0, column=0, sticky=W, padx=6)
Label(add_frame, text="No. of arguments", bg="white").grid(row=0, column=1, sticky=W, padx=6)
add_pred = ttk.Combobox(add_frame, values=list(PREDICATES), width=14, font=("Arial", 11))
add_pred.grid(row=1, column=0, padx=6, pady=(0, 6), sticky=EW)
add_arity = Spinbox(add_frame, from_=1, to=3, width=5, font=("Arial", 11), state="readonly")
add_arity.grid(row=1, column=1, padx=6, pady=(0, 6), sticky=W)
add_args = make_arg_entries(add_frame, 2)

preview = Label(add_frame, text="Preview: -", font=("Consolas", 13, "bold"), fg="#1a4fa0", bg="white")
preview.grid(row=4, column=0, columnspan=3, sticky=W, padx=6, pady=6)

btns = Frame(add_frame, bg="white")
btns.grid(row=5, column=0, columnspan=3, sticky=EW, pady=4)

# ---------------------------------------------------------------------------
# Right: list of facts
# ---------------------------------------------------------------------------
list_frame = LabelFrame(a, text=" Facts in the Knowledge Base ", font=("Arial", 12, "bold"), bg="white", padx=8, pady=8)
list_frame.grid(row=2, column=1, sticky=NSEW, padx=(7, 14), pady=4)
list_frame.rowconfigure(0, weight=1)
list_frame.columnconfigure(0, weight=1)
fact_list = Listbox(list_frame, font=("Consolas", 12), height=9, activestyle="none",
                    selectbackground="#1a4fa0")
fact_list.grid(row=0, column=0, sticky=NSEW)
sb = Scrollbar(list_frame, command=fact_list.yview)
sb.grid(row=0, column=1, sticky=NS)
fact_list.config(yscrollcommand=sb.set)
count_lbl = Label(list_frame, text="", bg="white", fg="#555")
count_lbl.grid(row=1, column=0, sticky=W, pady=(4, 0))
Label(list_frame, text="Tip: double-click a fact to copy it into the query box",
      bg="white", fg="#888", font=("Arial", 9)).grid(row=2, column=0, sticky=W)

# ---------------------------------------------------------------------------
# Bottom-left: Ask a query
# ---------------------------------------------------------------------------
q_frame = LabelFrame(a, text=" Ask a Query  (use ? as a wildcard) ", font=("Arial", 12, "bold"), bg="white", padx=8, pady=8)
q_frame.grid(row=3, column=0, sticky=NSEW, padx=(14, 7), pady=4)
Label(q_frame, text="Predicate", bg="white").grid(row=0, column=0, sticky=W, padx=6)
Label(q_frame, text="No. of arguments", bg="white").grid(row=0, column=1, sticky=W, padx=6)
q_pred = ttk.Combobox(q_frame, values=list(PREDICATES), width=14, font=("Arial", 11))
q_pred.grid(row=1, column=0, padx=6, pady=(0, 6), sticky=EW)
q_arity = Spinbox(q_frame, from_=1, to=3, width=5, font=("Arial", 11), state="readonly")
q_arity.grid(row=1, column=1, padx=6, pady=(0, 6), sticky=W)
q_args = make_arg_entries(q_frame, 2)
Checkbutton(q_frame, text="Ignore upper/lower case", variable=ignore_case, bg="white").grid(
    row=4, column=0, columnspan=2, sticky=W, padx=2)
result = Label(q_frame, text="Result will appear here", font=("Arial", 12, "bold"),
               fg="#555", bg="white", wraplength=400, justify=LEFT)
result.grid(row=6, column=0, columnspan=3, sticky=W, padx=6, pady=(6, 0))

# ---------------------------------------------------------------------------
# Bottom-right: predicate table
# ---------------------------------------------------------------------------
t_frame = LabelFrame(a, text=" Predicates ", font=("Arial", 12, "bold"), bg="white", padx=8, pady=8)
t_frame.grid(row=3, column=1, sticky=NSEW, padx=(7, 14), pady=4)
t_frame.columnconfigure(0, weight=1)
table = ttk.Treeview(t_frame, columns=("pred", "n", "meaning"), show="headings", height=7)
table.heading("pred", text="Predicate")
table.heading("n", text="No. of args")
table.heading("meaning", text="Meaning")
table.column("pred", width=90)
table.column("n", width=75, anchor=CENTER)
table.column("meaning", width=250)
table.grid(row=0, column=0, sticky=NSEW)

Label(a, textvariable=status, anchor=W, bg="#1a4fa0", fg="white", padx=10).grid(
    row=4, column=0, columnspan=2, sticky=EW, pady=(6, 0))


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------
def refresh_list():
    fact_list.delete(0, END)
    for f in sorted(facts):
        fact_list.insert(END, fact_to_text(f))
    count_lbl.config(text="Total facts: {}".format(len(facts)))


def refresh_table():
    table.delete(*table.get_children())
    for name, (n, m) in PREDICATES.items():
        table.insert("", END, values=(name, n, m.replace("{0}", "X").replace("{1}", "Y").replace("{2}", "Z")))


def on_pred_selected(event, box, arity_box, entries):
    """When a known predicate is chosen, set the number of argument boxes."""
    name = box.get().strip().capitalize()
    if name in PREDICATES:
        arity_box.config(state=NORMAL)
        arity_box.delete(0, END)
        arity_box.insert(0, PREDICATES[name][0])
        arity_box.config(state="readonly")
    set_arity(entries, int(arity_box.get()))
    update_preview()


def on_arity_changed(arity_box, entries):
    set_arity(entries, int(arity_box.get()))
    update_preview()


def update_preview(event=None):
    pred = add_pred.get().strip() or "?"
    n = int(add_arity.get())
    args = [e.get().strip() or "_" for e in add_args[:n]]
    preview.config(text="Preview: {}({})".format(pred, ", ".join(args)))


def add_fact(event=None):
    try:
        f = read_fact(add_pred, add_arity, add_args)
    except ValueError as err:
        messagebox.showwarning("Cannot add fact", str(err))
        return
    if f in facts:
        status.set("{} is already in the knowledge base".format(fact_to_text(f)))
        return
    if f[0] not in PREDICATES:            # new predicate typed by the user
        PREDICATES[f[0]] = (len(f) - 1, "user-defined predicate")
        add_pred.config(values=list(PREDICATES))
        q_pred.config(values=list(PREDICATES))
        refresh_table()
    facts.add(f)
    refresh_list()
    for e in add_args:
        if str(e.cget("state")) == NORMAL:
            e.delete(0, END)
    update_preview()
    status.set("Added fact: {}   ({})".format(fact_to_text(f), meaning(f)))


def delete_fact():
    sel = fact_list.curselection()
    if not sel:
        status.set("Select a fact in the list to delete it")
        return
    text = fact_list.get(sel[0])
    for f in list(facts):
        if fact_to_text(f) == text:
            facts.discard(f)
    refresh_list()
    status.set("Deleted fact: {}".format(text))


def clear_all():
    if messagebox.askyesno("Clear all", "Remove every fact from the knowledge base?"):
        facts.clear()
        refresh_list()
        status.set("Knowledge base cleared")


def same(x, y):
    return x.lower() == y.lower() if ignore_case.get() else x == y


def ask_query(event=None):
    try:
        q = read_fact(q_pred, q_arity, q_args, allow_wildcard=True)
    except ValueError as err:
        result.config(text=str(err), fg="#c0392b")
        return
    pattern = q[1:]
    matches = []
    for f in facts:
        if same(f[0], q[0]) and len(f) == len(q):
            if all(p == "?" or same(p, v) for p, v in zip(pattern, f[1:])):
                matches.append(f)
    if "?" not in pattern:                       # yes / no question
        if matches:
            result.config(text="TRUE  -  {} is a fact.\nMeaning: {}".format(
                fact_to_text(q), meaning(matches[0])), fg="#1e8449")
        else:
            result.config(text="FALSE  -  {} is not in the knowledge base.".format(
                fact_to_text(q)), fg="#c0392b")
    else:                                        # wildcard question
        if matches:
            lines = [fact_to_text(m) for m in sorted(matches)]
            result.config(text="{} match(es) for {}:\n{}".format(
                len(matches), fact_to_text(q), "\n".join(lines)), fg="#1a4fa0")
        else:
            result.config(text="No facts match {}".format(fact_to_text(q)), fg="#c0392b")
    status.set("Query asked: {}".format(fact_to_text(q)))


def load_into_query(event):
    """Double-click on a fact copies it into the query section."""
    sel = fact_list.curselection()
    if not sel:
        return
    text = fact_list.get(sel[0])
    for f in facts:
        if fact_to_text(f) == text:
            q_pred.set(f[0])
            on_pred_selected(None, q_pred, q_arity, q_args)
            for e, v in zip(q_args, f[1:]):
                e.delete(0, END)
                e.insert(0, v)
            status.set("Copied {} into the query box".format(text))
            return


def save_facts():
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if path:
        with open(path, "w") as fh:
            for f in sorted(facts):
                fh.write(fact_to_text(f) + "\n")
        status.set("Saved {} facts to {}".format(len(facts), path))


def load_facts():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not path:
        return
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.endswith(")") and "(" in line:
                name, rest = line[:-1].split("(", 1)
                args = [x.strip() for x in rest.split(",")]
                facts.add(tuple([name] + args))
                PREDICATES.setdefault(name, (len(args), "user-defined predicate"))
    refresh_list()
    refresh_table()
    status.set("Loaded facts from {}".format(path))


# Buttons
Button(btns, text="Add Fact", bg="#1a4fa0", fg="white", font=("Arial", 11, "bold"),
       command=add_fact).pack(side=LEFT, expand=True, fill=X, padx=4)
Button(btns, text="Delete Selected", bg="#e67e22", fg="white", font=("Arial", 11),
       command=delete_fact).pack(side=LEFT, expand=True, fill=X, padx=4)
Button(btns, text="Clear All", bg="#c0392b", fg="white", font=("Arial", 11),
       command=clear_all).pack(side=LEFT, expand=True, fill=X, padx=4)
Button(q_frame, text="Ask", bg="#1e8449", fg="white", font=("Arial", 11, "bold"), width=10,
       command=ask_query).grid(row=4, column=2, sticky=E, padx=6)

# Event bindings
add_pred.bind("<<ComboboxSelected>>", lambda e: on_pred_selected(e, add_pred, add_arity, add_args))
add_pred.bind("<KeyRelease>", update_preview)
add_arity.config(command=lambda: on_arity_changed(add_arity, add_args))
for e in add_args:
    e.bind("<KeyRelease>", update_preview)
    e.bind("<Return>", add_fact)
q_pred.bind("<<ComboboxSelected>>", lambda e: on_pred_selected(e, q_pred, q_arity, q_args))
q_arity.config(command=lambda: on_arity_changed(q_arity, q_args))
for e in q_args:
    e.bind("<Return>", ask_query)
fact_list.bind("<Double-Button-1>", load_into_query)
fact_list.bind("<Delete>", lambda e: delete_fact())

# Menu bar
menubar = Menu(a)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Save facts...", command=save_facts)
file_menu.add_command(label="Load facts...", command=load_facts)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=a.destroy)
menubar.add_cascade(label="File", menu=file_menu)
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
    "About", "Knowledge Base GUI\nStores facts as predicates and answers queries.\nBuilt with Python Tkinter."))
menubar.add_cascade(label="Help", menu=help_menu)
a.config(menu=menubar)

# Initial state
add_pred.set("Likes")
on_pred_selected(None, add_pred, add_arity, add_args)
q_pred.set("Professor")
on_pred_selected(None, q_pred, q_arity, q_args)
refresh_list()
refresh_table()

if __name__ == "__main__":
    a.mainloop()
