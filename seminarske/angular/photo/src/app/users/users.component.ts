import {Component, OnInit} from '@angular/core';
import {User} from '../user';
import {UserService} from '../user.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

//objekt za slike in predpona naslovov slik, ker se nahjajo na "drugem" strežniku
  users: User[];
  userHost = UserService.userHost;


  constructor(private userService: UserService) {
  }

  getUsers(): void {
    this.userService.getUsers()
      .subscribe(users => this.users = users);
  }

  ngOnInit() {
    this.getUsers();
  }
}
