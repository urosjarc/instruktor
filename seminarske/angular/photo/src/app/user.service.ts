import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {User} from './user';
import {catchError, map, tap} from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class UserService {

//naslov storitve
  public static userHost = 'http://localhost:3000/';

  //Injectan http client za ajax zahteve
  constructor(
    private http: HttpClient) {
  }

//enostavna zahteva na strežnik, ki vrača json seznam vseh slik
  public getUsers(): Observable<User[]> {
    return this.http.get<User[]>(UserService.userHost + 'users');
  }

//enostavna zahteva na strežnik, ki vrača json objekt ene slike
  public getUser(_id: string): Observable<User> {
    return this.http.get<User>(UserService.userHost + 'users/' + _id);
  }

}
