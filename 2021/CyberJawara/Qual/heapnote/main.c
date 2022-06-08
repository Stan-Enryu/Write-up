#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct note {
  char title[32];
  char content[72];
} note_t;

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
}

size_t read_uint(char *prompt) {
  char buf[16];
  printf("%s", prompt);
  read(STDIN_FILENO, buf, 15);
  return strtoul(buf, NULL, 10);
}

void print_notes(note_t **notes) {
  printf("      ,-----------.\n");
  printf("     (_\\  heapnote \\\n");
  printf("       |           |\n");
  for (int i = 0; i < 10; i++)
    printf("       | %d. %.6s |\n", i, notes[i]->title);
  printf("      _|           |\n");
  printf("     (_/_____(*)___/\n");
  printf("              \\\\\n");
  printf("               ))\n");
  printf("               ^\n");
}

void delete_note(note_t **notes) {
  size_t idx = read_uint("idx = ");
  if (!notes[idx] || idx >= 10) return;

  free(notes[idx]);
}

void add_note(note_t **notes) {
  size_t idx = read_uint("idx = ");
  if (idx >= 10) return;

  note_t *note = malloc(sizeof(note_t));
  if (!note) {
    exit(1);
  }

  printf("title = ");
  read(STDIN_FILENO, note->title, sizeof(note->title) - 1);
  printf("content = ");
  read(STDIN_FILENO, note->content, sizeof(note->content) - 1);

  notes[idx] = note;
}

int main(int argc, char const *argv[]) {
  note_t *notes[10];
  size_t choice;

  setup();
  for (int i = 0; i < 10; i++) notes[i] = NULL;

  for (;;) {
    print_notes(notes);
    choice = read_uint("> ");
    switch (choice) {
      case 1:
        add_note(notes);
        break;
      case 2:
        delete_note(notes);
        break;
      default:
        puts("nope");
        break;
    }
  }

  return 0;
}
