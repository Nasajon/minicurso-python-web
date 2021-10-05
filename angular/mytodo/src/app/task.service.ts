import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Task } from './task';
import { TASKS } from './mock-tasks';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  private tasksUrl = '/api/tasks';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient
  ) { }

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.tasksUrl).pipe(
      catchError(this.handleError<Task[]>('getTasks', []))
    );
  }

  getTask(id: String): Observable<Task> {
    const url = `${this.tasksUrl}/${id}`;
    return this.http.get<Task>(url).pipe(
      catchError(this.handleError<Task>(`getTask id=${id}`))
    );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);

      return of(result as T);
    };
  }

  updateTask(task: Task): Observable<any> {
    const url = `${this.tasksUrl}/${task.id}`;
    return this.http.put(url, task, this.httpOptions).pipe(
      catchError(this.handleError<any>('updateTask'))
    );
  }

  /** POST: add a new task to the server */
  addTask(task: Task): Observable<Task> {
    return this.http.post<Task>(this.tasksUrl, task, this.httpOptions).pipe(
      catchError(this.handleError<Task>('addTask'))
    );
  }

  /** DELETE: delete the hero from the server */
  deleteTask(id: string): Observable<Task> {
    const url = `${this.tasksUrl}/${id}`;

    return this.http.delete<Task>(url, this.httpOptions).pipe(
      catchError(this.handleError<Task>('deleteTask'))
    );
  }
}
