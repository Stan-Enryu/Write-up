struct _IO_FILE
{
  int _flags;                /* High-order word is _IO_MAGIC; rest is flags. */
  /* The following pointers correspond to the C++ streambuf protocol. */
  char *_IO_read_ptr;        /* Current read pointer */
  char *_IO_read_end;        /* End of get area. */
  char *_IO_read_base;        /* Start of putback+get area. */
  char *_IO_write_base;        /* Start of put area. */
  char *_IO_write_ptr;        /* Current put pointer. */
  char *_IO_write_end;        /* End of put area. */
  char *_IO_buf_base;        /* Start of reserve area. */
  char *_IO_buf_end;        /* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */
  struct _IO_marker *_markers;
  struct _IO_FILE *_chain;
  int _fileno;
  int _flags2;
  __off_t _old_offset; /* This used to be _offset but it's too small.  */
  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];
  _IO_lock_t *_lock;
#ifdef _IO_USE_OLD_IO_FILE
};
---------------------------------------------------------------------------
-- puts
static
_IO_size_t
new_do_write (_IO_FILE *fp, const char *data, _IO_size_t to_do)
{
  _IO_size_t count;
  if (fp->_flags & _IO_IS_APPENDING)
    ...
  else if (fp->_IO_read_end != fp->_IO_write_base) // harus false
    {
      _IO_off64_t new_pos = _IO_SYSSEEK (fp, fp->_IO_write_base - fp->_IO_read_end, 1);
      ...
    }
  count = _IO_SYSWRITE (fp, data, to_do);
  ...
}

data = f->_IO_write_base
to_do = f->_IO_write_ptr - f->_IO_write_base
_IO_do_write (f, f->_IO_write_base, f->_IO_write_ptr - f->_IO_write_base);

assert(f->_IO_write_ptr > f->_IO_write_base)

---------------------------------------------------------------------------
-- fgets
int
_IO_new_file_underflow (_IO_FILE *fp)
{
  ...
  count = _IO_SYSREAD (fp, fp->_IO_buf_base, fp->_IO_buf_end - fp->_IO_buf_base);
  ...
}

assert(fp->_IO_buf_end > fp->_IO_buf_base)

---------------------------------------------------------------------------

setcontext
...
0x00007ffff7defe35 <+53>:    mov    rsp,QWORD PTR [rdx+0xa0]
0x00007ffff7defe3c <+60>:    mov    rbx,QWORD PTR [rdx+0x80]
0x00007ffff7defe43 <+67>:    mov    rbp,QWORD PTR [rdx+0x78]
0x00007ffff7defe47 <+71>:    mov    r12,QWORD PTR [rdx+0x48]
0x00007ffff7defe4b <+75>:    mov    r13,QWORD PTR [rdx+0x50]
0x00007ffff7defe4f <+79>:    mov    r14,QWORD PTR [rdx+0x58]
0x00007ffff7defe53 <+83>:    mov    r15,QWORD PTR [rdx+0x60]
0x00007ffff7defe57 <+87>:    mov    rcx,QWORD PTR [rdx+0xa8]
0x00007ffff7defe5e <+94>:    push   rcx
0x00007ffff7defe5f <+95>:    mov    rsi,QWORD PTR [rdx+0x70]
0x00007ffff7defe63 <+99>:    mov    rdi,QWORD PTR [rdx+0x68]
0x00007ffff7defe67 <+103>:   mov    rcx,QWORD PTR [rdx+0x98]
0x00007ffff7defe6e <+110>:   mov    r8,QWORD PTR [rdx+0x28]
0x00007ffff7defe72 <+114>:   mov    r9,QWORD PTR [rdx+0x30]
0x00007ffff7defe76 <+118>:   mov    rdx,QWORD PTR [rdx+0x88]
0x00007ffff7defe7d <+125>:   xor    eax,eax
0x00007ffff7defe7f <+127>:   ret    
0x00007ffff7defe80 <+128>:   mov    rcx,QWORD PTR [rip+0x18dfe9]        # 0x7ffff7f7de70
0x00007ffff7defe87 <+135>:   neg    eax
0x00007ffff7defe89 <+137>:   mov    DWORD PTR fs:[rcx],eax
0x00007ffff7defe8c <+140>:   or     rax,0xffffffffffffffff
0x00007ffff7defe90 <+144>:   ret 

---------------------------------------------------------------------------
int
_IO_puts (const char *str)                                                    
{                                                                              
  ...                                              
  if (...                                     
      && _IO_sputn (_IO_stdout, str, len)
      ...
      )
  ...                                                             
}  

_IO_size_t
_IO_new_file_xsputn (_IO_FILE *f, const void *data, _IO_size_t n)
{
  ...
  else if (f->_IO_write_end > f->_IO_write_ptr) //false
    count = f->_IO_write_end - f->_IO_write_ptr;
  ...
      if (_IO_OVERFLOW (f, EOF) == EOF) 
  ...
}

int
_IO_new_file_overflow (_IO_FILE *f, int ch)
{
  if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL)
  {
      ...
  {
  ...
  if (ch == EOF)
    return _IO_do_write (f, f->_IO_write_base, f->_IO_write_ptr - f->_IO_write_base);
  ...
}

rdi = f->_IO_write_ptr - f->_IO_write_base